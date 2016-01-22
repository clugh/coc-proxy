Interceptor.attach(ptr(addr),
{
    onEnter(args)
    {
        this.pk = args[0];
        this.sk = args[1];
    },
    onLeave(retval)
    {
        send("sk", Memory.readByteArray(this.sk, 32));
        var op = recv(function(){});
        op.wait();
    }
});
