# DNSCountryFilter
A DNS Proxy with country filtering capabilities

The main process is in proxy.py. The country list is hard coded as countries.dat in my home directory (Move this wherever you want)

The proxy listens on 5323 because it's easier for testing without root. Ideally you would make the proxy listen on port 53 and send requests to a pihole or upstream
dns server (if running on the same machine you will need it running on a different port).

ipgeolocation.py contains the country lookup portions and some unused dns stuff that I will eventually remove. It uses http and json to capture just the country code
(CN, RU, US, etc). If the country returned exists in the countries.dat file, the dns record will be removed and not returned to the client. 

For examples returning several different IP's only ones that match blocked countries will be removed.

For performance I will eventually move the loading and uloading of the countries.dat file out of the handler loop so that it's not reloaded each time a query comes in.


Feel free to steal this code as it's already mostly stolen from various other projects around the internet.
