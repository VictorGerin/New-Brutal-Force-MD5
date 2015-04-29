It's very simple to use

let's try to crack this hash 'ffc150a160d37e92012c196b6af4160d' <- 'victor'

python quebra.py -l ffc150a160d37e92012c196b6af4160d

here a only use the -l option that means use only small letters and finely the hash other options can be

-n <- Use number
-L <- Use big letters
-e <- Use accentuation

you can combine then

like

python quebra.py -lLn ffc150a160d37e92012c196b6af4160d

Let's look at more advanced options

With

-min [number] and -max [number]

you can set the minimum size of all sons or then max size

or you can use -fixSize [number] is the same to set min and max equals

-seed [key] This option will set the fist seed if you know some part of key Example
python quebra.py -l -seed 'vict' ffc150a160d37e92012c196b6af4160d
you can set the option -useSeomenteSeed (in English 'use only seed') to use only the seed as father

-addChar [number] The number of chars the random gen will add in sons keys

-filhos [number] (in English 'sons') set the max number that sons one key can have in one generation

-genMax [number] set the maximum generation that one key can have before discard it

-genMaxEspecial [number] (in English Especial = special) if the actual son is the best found yet so then is considerate special so because that i set a different number of generation before discard it

Now let's look in more advanced option over the last :)

as than use random key generator its need know whats keys already used, to do that i keep all data in a database, so, all option, by now is referent to database

-numCommit [number] The number of sons generated until i do the commit

-db [db name] By default i keep the database in memory (using Sqlite) but it's possible set a file to use as sqlite database, to do so may leave the program slower, but is the only option if do you not have a good computer

-getDbToMemory [db name] That option get a db from a slqite file and put in memory, use memory is good why the program can run faster, so if you stooped and want restart and using the memory and don't lose all data generate and tested you can save all date, and backup late use this option

-pula (In English 'jump or skip') that skip the first verification of the database have the hash (be careful if the hash is in database the program never will find it)

When you hit 'ctrl + c' in terminal to finalize the program will ask first if you want export the actual database to another (this is helpful if you want do a back of memory database to a file) the ask if "Gostaria de copiar o banco de dados para outro lugar ?" in English "Do you want copy the database to another place ?"

And if you use the -getDbToMemory [db name] option then will ask to "Gostaria voltar o banco de dados para o arquivo original ?" in English "Do you want back the database to original file ?" that option will copy all database that is in memory to the original file
