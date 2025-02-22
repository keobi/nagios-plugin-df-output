# nagios-plugin-df-output

Nagios plugin to check the usage percent output of the `df -h` command.

## Installation

On your _host_:

1. Clone this repository
1. Create a symlink of `check_df_output.py` to your plugin directory (typically `/usr/lib/nagios/plugins/`)

On your Icinga instance (using Director):

1. Define three new data fields in Icinga Director: `df_partition` (string), `df_critical` (number), and `df_warning` (number)
1. Create the command (below)
1. Create the service template and add the data fields
1. Add to your service set or directly to a host

### Command

```
object CheckCommand "df_output" {
    import "plugin-check-command"
    command = [ PluginDir + "/check_df_output.py" ]
    arguments += {
        "(no key)" = {
            description = "partition"
            required = true
            skip_key = true
            value = "$df_partition$"
        }
        "-c" = {
            description = "Critical value"
            required = true
            value = "$df_critical$"
        }
        "-w" = {
            description = "Warning"
            required = true
            value = "$df_warning$"
        }
    }
}
```

## Use Case

This plugin checks the output of `df -h` for the usage of a particular partition. 

`df -h` output:

```
Filesystem       Size  Used Avail Use% Mounted on
/dev/root         29G   17G   13G  56% /
tmpfs            7.8G     0  7.8G   0% /dev/shm
tmpfs            6.0G  1.2M  6.0G   1% /run
tmpfs            5.0M     0  5.0M   0% /run/lock
```

If we wanted to check the usage of the `/run` partition, we would use the following command:

```
check_df_output.py /run -c 90 -w 80
```