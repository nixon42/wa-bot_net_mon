:if ([:len $this ]>0) do={
:local chars " \"%&"; 
:local subs { "%20"; "'"; "%25"; "%26" }
:local that "";
:for i from=0 to=([:len $this]-1) do={ 
	:local s [:pick $this $i];
	:local x [:find $chars $s]
	:if ([:len $x]>0) do={
		:set $s ($subs->$x)	
	}
	:set $that ($that . $s)
}
:return $that;
}