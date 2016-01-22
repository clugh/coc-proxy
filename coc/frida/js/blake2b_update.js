Interceptor.attach(ptr(addr),
{
    onEnter(args)
    {
        this.state = args[0]
        this.in = args[1];
        this.length = args[2];
        send("in", Memory.readByteArray(this.in, this.length.toInt32()));
    }
});
