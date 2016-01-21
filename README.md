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
    echo 0c3cb9f72bf6930ccd8567a520c35542e3b02b4a407837af1233c783c459810c | xxd -r -p > key-new.bin
    xxd -p -c 32 key-new.bin
    dd if=key-new.bin of=libg.so seek=3624982 bs=1 count=32 conv=notrunc
    adb push libg.so /data/data/com.supercell.clashofclans/lib/libg.so

You may need to adjust the offset or remote location based on version or arch.  For example, the file is stored at `/data/app-lib/com.supercell.clashofclans-2/libg.so` on `Kitkat` and the offset is `5645304` on `x86`.
