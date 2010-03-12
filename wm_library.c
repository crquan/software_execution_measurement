int request_initialise_wm();
int request_update_wm(int, char *, int);
int request_retrieval_wm(int, int *);
int request_release_wm(int);

static int watermark_value;

int request_initialise_wm()
{
    watermark_value = 0;
    return 0;
}

int request_update_wm(int wmid, char *buf, int length)
{
    int i;

    if(wmid != 0)
    {
        return 1;
    }

    for(i = 0; i < length; i ++)
    {
        watermark_value <<= 1;
        if(buf[i] == '0')
            watermark_value &= (~0x1ULL);
        else if (buf[i] == '1')
            watermark_value |= 0x1;
        else
            return 1;
    }

    return 0;
}

int request_retrieval_wm(int wmid, int *val)
{
    if(wmid != 0)
    {
        return -1;
    }

    *val = watermark_value;
    return 0;
}

int request_release_wm(int wmid)
{
    if(wmid != 0)
    {
        return -1;
    }

    watermark_value = 0;
    return 0;
}
