#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/sched.h>
#include <linux/list.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>
#include <linux/uaccess.h>

#define MAXIMUM_BITS 32

struct entropy_record {
	unsigned long bits[ MAXIMUM_BITS / BITS_PER_LONG];
	pid_t pid;
	struct list_head entry;
};

static LIST_HEAD(global_head);

static int misc_open(struct inode *inode, struct file *file)
{
	struct entropy_record *ptr;

	ptr = kmalloc(sizeof(*ptr), GFP_KERNEL);
	if (!ptr) {
		return -ENOMEM;
	}
	ptr->pid = current->pid;
	list_add(&ptr->entry, &global_head);

	return 0;
}

static int misc_release(struct inode *inode, struct file *file)
{
	/* TODO: properly cleanup */
	return 0;
}

static ssize_t misc_read(struct file *file, char __user *buf, size_t len, loff_t *pos)
{
	return 0;
}

static ssize_t misc_write(struct file *file, const char __user *buf, size_t len, loff_t *pos)
{
	/* input len for 1..N */
	struct entropy_record *ptr;
	list_for_each_entry(ptr, &global_head, entry) {
		if (ptr->pid == current->pid) {
			char bit;
			get_user(bit, buf);
			bit = (bit == '1' ? 1 :
					(bit == '0' ? 0 : -1));
			/* if not 0,1, error handling */
			ptr->bits[0] = ptr->bits[0] << 1 | bit;
		}
	}
	return len;
}

/*
 * interface for entry bits reset
 */
static long misc_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
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

fail:
	return 0;
}

static void __exit misc_exit(void)
{
	misc_deregister(&_misc);
}

module_init(misc_init);
module_exit(misc_exit);

MODULE_LICENSE("GPL");
