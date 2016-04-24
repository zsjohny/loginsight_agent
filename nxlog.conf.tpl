define ROOT  /etc/nxlog

define CERTDIR /etc/nxlog/data/CA


Moduledir /usr/lib/nxlog/modules/
#/usr/lib/nxlog/modules

CacheDir %ROOT%/data

Pidfile %ROOT%/data/nxlog.pid

SpoolDir %ROOT%/data

LogFile %ROOT%/data/nxlog.log

#LogLevel DEBUG

<Processor evcorr>
    Module        pm_evcorr
    <Simple>
        Exec $raw_event = "FILE="+$FileName+" "+"HOST="+$HostName+" "+"KEY="+$StreamKey+" "+"TYPE="+$StreamType+" "+"TAG="+$StreamTag+" "+$raw_event;
    </Simple>
</Processor>

########### You can add logfile to new block #########
<Input in>
    Module       im_file
    File         '{{ LOG_PATH }}'
    SavePos        TRUE
    PollInterval 1
    # Explicitly set the Hostname. This defaults to the system's hostname if unset.
    Exec    $HostName = '{{ HOSTNAME }}';
    Exec    $StreamKey = '{{ STREAMKEY }}';
    Exec    $StreamType = '{{ SREAMTYPE }}';
    Exec    $StreamTag = '{{ STREAMRAG }}';
    Exec    $FileName = file_name();
</Input>
########## END ###########

<Output sslout>
    Module	om_ssl
    Host	139.129.93.241
    Port	12000
    CAFile	%CERTDIR%/cacert.pem
    CertFile	%CERTDIR%/server.crt
    CertKeyFile %CERTDIR%/server.key
    KeyPass	secret
    AllowUntrusted  TRUE
    OutputType	Binary
</Output>

<Route 1>
    Path        in => evcorr => sslout
</Route>

