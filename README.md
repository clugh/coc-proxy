# coc-proxy

Run with:

    python3.5 proxy.py

## Installation

Install `twisted` with:

    python3.5 -m pip install twisted

Install `pynacl` with:

    python3.5 -m pip install pynacl

Install `pyblake2` with:

    python3.5 -m pip install pyblake2

Patch `libg.so` with:

    adb pull /data/data/com.supercell.clashofclans/lib/libg.so
    dd if=libg.so of=key-backup.bin skip=3624982 bs=1 count=32
    xxd -p -c 32 key-backup.bin
    echo 72f1a4a4c48e44da0c42310f800e96624e6dc6a641a9d41c3b5039d8dfadc27e | xxd -r -p > key-new.bin
    xxd -p -c 32 key-new.bin
    dd if=key-new.bin of=libg.so seek=3624982 bs=1 count=32 conv=notrunc
    adb push libg.so /data/data/com.supercell.clashofclans/lib/libg.so

You may need to adjust the offset or remote location based on version or arch.  For example, the file is stored at `/data/app-lib/com.supercell.clashofclans-2/libg.so` on `Kitkat` and the offset is `5645304` on `x86`. See the [Key Offsets](https://github.com/clugh/coc-proxy/wiki/Key-Offsets) wiki page for more information.

###Routing Packets

This topic is expansive and is outside the scope of this document.  See the [Routing Packets](https://github.com/clugh/coc-proxy/wiki/Routing-Packets) wiki page on the for more information.
