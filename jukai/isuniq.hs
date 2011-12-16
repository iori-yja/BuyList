uniqlist::[String]->[String]->[String]
uniqlist xs  [] = xs
uniqlist as (b:bs) = if isuniq b as
		    then uniqlist (b:as) (tail bs)
		    else uniqlist as (tail bs)
