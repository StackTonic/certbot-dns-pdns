# certbot-pdns

Plugin to allow acme dns-01 authentication of a name managed with PowerDNS. 

## Named Arguments
| Argument | Description |
| --- | --- |
| --dns-pdns-credentials &lt;file&gt; | pdns credentials INI file **(required)** |

## Install
``` bash
pip install certbot-dns-pdns
```
## Credentials
Download the file `credentials.ini.exemple` and rename it to `credentials.ini`. Edit it to set your pdns url and API Key.
```
# The API URL
# include the scheme and the port number (usually 8081 for https)
dns_pdns_api = https://api.exemple.com:8081

# The API KEY
dns_pdns_key = SomethingSecureHere
```

## Additional documentation
* https://doc.powerdns.com/authoritative/http-api/index.html
* https://certbot.eff.org/docs/