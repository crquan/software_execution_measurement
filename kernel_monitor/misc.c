#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/sched.h>
#include <linux/list.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/uaccess.h>

#define MAXIMUM_BITS 32

struct entropy_record {
	unsigned int bits[MAXIMUM_BITS / BITS_PER_LONG];
	pid_t pid;
	struct list_head entry;
};

static LIST_HEAD(global_head);

/*
 * some helpers to dump internal structures
 */
static void dump_er(struct entropy_record *entry)
{
	printk("dump entry %p, bits[0] %#x, pid %d, list_head <%p,%p>\n",
			entry, entry->bits[0], entry->pid,
			entry->entry.prev, entry->entry.next);
}

static void dump_er_all(void)
{
	struct entropy_record *ptr;

	printk("Dump er all:\n");
	list_for_each_entry(ptr, &global_head, entry)
		dump_er(ptr);
}

static int misc_open(struct inode *inode, struct file *file)
{
	struct entropy_record *ptr;

	ptr = kzalloc(sizeof(*ptr), GFP_KERNEL);
	if (!ptr) {
		return -ENOMEM;
	}
	memset(ptr, '\0', sizeof (*ptr));
	ptr->bits[0] = 0;
	ptr->pid = current->tgid;
	dump_er(ptr);
	printk("initialized program %d, ptr %p, bits = %#x\n", ptr->pid, ptr, ptr->bits[0]);
	list_add(&ptr->entry, &global_head);
	ptr->bits[0] = 0;
	dump_er(ptr);
	printk("initialized program %d, ptr %p, bits = %#x\n", ptr->pid, ptr, ptr->bits[0]);
	dump_er(ptr);

	return 0;
}

static int misc_release(struct inode *inode, struct file *file)
{
	/* TODO: properly cleanup */

	/* chain out all current process list entry, and free */
	struct entropy_record *ptr, *n;
	list_for_each_entry_safe(ptr, n, &global_head, entry) {
		if (ptr->pid == current->tgid) {
			printk("program %d exit\n", ptr->pid);
			list_del(&ptr->entry);
			kfree(ptr);
		}
	}

	return 0;
}

static ssize_t misc_read(struct file *file, char __user *buf, size_t len, loff_t *pos)
{
	int num;
	struct entropy_record *ptr;

	printk("program %d read\n", current->tgid);
	/* input len for 1 integer, sizeof(int) == 4 */
	list_for_each_entry(ptr, &global_head, entry) {
		if (ptr->pid == current->tgid) {
			num = ptr->bits[0];
			put_user(num, buf);
			printk("user retrieve, give num = %#x\n", num);
			break;
		}
	}

	return sizeof(num);
}

static ssize_t misc_write(struct file *file, const char __user *buf, size_t len, loff_t *pos)
{
	struct entropy_record *ptr;

	printk("program %d write\n", current->tgid);

	/* input len for 1..N */
	list_for_each_entry(ptr, &global_head, entry) {
		if (ptr->pid == current->tgid) {
			char bit = '\0';
			get_user(bit, buf);
			bit = (bit == '1' ? 1 :
					(bit == '0' ? 0 : -1));
			/* if not 0,1, error handling */
			ptr->bits[0] = ptr->bits[0] << 1 | bit;
			printk("got user buf: %#x, updated bits: %#x\n", bit, ptr->bits[0]);
			break;
		}
	}
	return len;
}

#define IOCTL_RESET 0x3f2f0783

/*
 * interface for entry bits reset
 */
static long misc_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
	switch (cmd) {
		case IOCTL_RESET:
			;
		default:
			;
	}

	return 0;
}

static struct file_operations ops = {
	.open = misc_open,
	.release = misc_release,
	.read = misc_read,
	.write = misc_write,
	.unlocked_ioctl = misc_ioctl,
};

static struct miscdevice _misc = {
	.minor = MISC_DYNAMIC_MINOR,
	.name = "execution-trace-monitor",
	.fops = &ops,
};

static int __init misc_init(void)
{
	int ret;

	ret = misc_register(&_misc);
	if (ret < 0) {
		goto fail;
	}

	printk("Kernel Execution trace monitor started, global_head %p\n",
			&global_head);

fail:
	return 0;
}

static void __exit misc_exit(void)
{
	/* before exit, to cleanup all; */
	struct entropy_record *ptr, *n;

	dump_er_all();

	list_for_each_entry_safe(ptr, n, &global_head, entry) {
		list_del(&ptr->entry);
		kfree(ptr);
	}

	misc_deregister(&_misc);
}

module_init(misc_init);
module_exit(misc_exit);

MODULE_LICENSE("GPL");
