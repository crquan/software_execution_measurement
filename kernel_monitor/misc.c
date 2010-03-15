#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/miscdevice.h>

static int misc_open(struct inode *inode, struct file *file)
{
	return 0;
}

static int misc_release(struct inode *inode, struct file *file)
{
	return 0;
}

static ssize_t misc_read(struct file *file, char __user *buf, size_t len, loff_t *pos)
{
	return 0;
}

static ssize_t misc_write(struct file *file, const char __user *buf, size_t len, loff_t *pos)
{
	return len;
}

static struct file_operations ops = {
	.open = misc_open,
	.release = misc_release,
	.read = misc_read,
	.write = misc_write,
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

MODULE_AUTHOR("CHENG Renquan <rqcheng@smu.edu.sg>");
MODULE_LICENSE("GPL");
