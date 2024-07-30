# test_rejunity_ay8913

Test code for the [tt_um_rejunity_ay8913 project](https://tinytapeout.com/runs/tt05/tt_um_rejunity_ay8913) an implementation of the AY-3-8913 (a 3-voice programmable sound generator chip from General Instruments) on [Tiny Tapeout 05](https://tinytapeout.com/runs/tt05/tt_um_rejunity_ay8913), running on micropython on the RP2040.

This will let you either play with the AY8913 interface directly or just call functions to play tunes.

NOTE: this all assumes you're running a TT demoboard, with [the SDK](https://github.com/TinyTapeout/tt-micropython-firmware/) installed.

## Play tunes

You'll need a file, such as that found in samples/ here, of the right format or to figure out how to get the register values to set for each time tick on your own.

The "psym" format is a derivative of YM files, such as those [found here](http://antarctica.no/stuff/atari/YM2/).  There's some complexity and processing involved in these things, which we don't have time for on the RP2040.  So I wrote [convertym](https://github.com/psychogenic/convertym) that takes in a ym file, uses the pretty sweet [StSoundLibrary](https://github.com/arnaud-carre/StSound/tree/main/StSoundLibrary) and dumps out a file that's just an uncompressed sequence of register settings.

To use the player, you can simply load your psym file onto the RP2040 fs and then do:

```
import tt_um_rejunity_ay8913.play_psym as player

player.run('/path/to/file.psym')

```

## Set registers manually

There are two implementations of the API -- a pure python and a PIO-based.  The PIO is fast (like 40us to set a register vs close to 8ms using the pure Python SDK).  Both support a simple

```
    set_register(regid, value)
```

method that does the right thing.  For more, use the source.

