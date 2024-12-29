# turing_complete_guitar

from some dude on hackernews claiming to show that guitar tab (specifically, the names of power (5ths) chords and a mm:ss designation at which to play them) is Turing Complete. Forked from his repo, I made a few improvements then began a similar project entirely anew. His post claiming that Guitar Tab is Tuning - er *Turing* - Complete then nerdsniped me for the rest of the day and part of the next.

I started off with the time/tempo/tuning stuff I'm about to mention, then quickly went off the rails. I stopped messing with it a couple of weeks ago, but there are some decent ideas presented in my pursuit to try to push his Turing-Completeness claim a little closer to truth (by defining the "machine" as the person and the guitarcpu, or adding a capo, pondering a looper pedal and the notation for integrating it into a guitar performance. In the end, I realized the "problem" wasn't at all interesting enough to justify my spending that much time on it, so I wrapped it up. Stumbling across the code now I recognize that amidst the silly and pointless is some actually useful code that I may come to use for some other project, or someone else out there may do the same so I created the github repo linked below and pushed that code to it.

## this repo

In *this* repo, only a few changes were made to the code which I forked from the author of that post. I converted it to use a more musical time/tempo format, added alternate tuning support and made some other changes, documented in the [comment thread for the aforementioned post](https://news.ycombinator.com/item?id=42294766)

## that repo

Then I went nuts with it, documenting *that* journey in [a repo of its own called gtrsnipe](https://github.com/scottvr/gtrsnipe) - "guttersnipe". I am putting guttersnipe online so that the potentially useful code that arose from it might see use by myself or someone else; it will be there when someone needs it and searches something close enough to what's there. 

### Among the useful are:
- a MIDI to Guitar Tab converter
- a FretboardMapper, which can be used to influence decisions made when shoosing a fret position for the next incoming note from a midi file being read
- an ABC to MIDI class
- the inverse capability from the above two items,
- an ascii tab renderer
- more

### mostly useless but potentially interesting are:
- a virtual ("guitar") CPU
- a compiler for it
- another compiler for it
- a Turing Machine ISA including the operations
   - LOAD
   - STORE
   - ADD
   - SUB
   - MUL
   - DIV
   - CMP
   - JMP
-  code writen in Python can be transpiled to a guitarcpu program, which consists of a series of note events (fret positions and fretting techniques), presented linearly at a tempo which can then be
    - output as guitar tab
    - output as a midi file
- music encoded in a MIDI file can be converted to
  - guitar tab
  - a series of musical events whcih can be mapped to GuitarCPU operations.
    - why would anybody want this?
      these capabilities mean that one can
        - take working python code and see what it sounds like
            - played on guitar from reading tab
            - as a midi file
        - take a song as midi data or guitar tab
            - convert it to whichever it is not
            - including GuitarCPU program instruction listing
            - and by extention, python code if you wish
  - a few different takes and incomplete versions of some of the aforementioned stuff

