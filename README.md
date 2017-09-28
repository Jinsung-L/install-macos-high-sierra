# install-macos-high-sierra
Solution for errors of macOS High Sierra Installation.
This instruction is based on my personal expirience.

## Backgrounds
- Upgrade from previous macOS. In my case, macOS Sierra.
- Upgrade using **macOS High Sierra Installer** downloaded from App Store.
- Upgrade went wrong during its progress. Black screen apeared. It tells you should diagnose or restart.

But after you restart it...

## Check your conditions
- Not able to boot. Screen shows question mark folder.
- Not able to boot in Safe Mode either.
- Able to boot in Recovery Mode.
- Able to reinstall in Recovery Mode.
- But it takes forever. The progress stops.
- Last log says `Retrying http://swcdn.apple.com/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/InstallESDDmg.pkg after 1 failure(s)` or something similar.

If your condition follows all above then follow [Downloading Stuck](#downloading-stuck)

If you somehow passed above stuations, but still...
- Requires `disk password`.
- Your password doesn't work. Including your Account password, FileValut password, iCloud password.
- Reset Password Mode doesn't help. All the three options are not available.
- Safe Mode results the same.
- Able/Not able to boot in Recovery Mode.
- Previously encrypted your disk using FileValut. (maybe doesn't matter)

If your condition follows all above then follow [Disk Password is Required](#disk-password-is-required)

### Notes
You can get into Recovery Mode by following this method. [Start up from macOS Recovery](https://support.apple.com/en-us/HT204904#recovery)
I tried all options. **_Command (⌘)-R_** and **_Option-Command-R_** were showing the same result, while *Shift-Option-Command-R* didn't work at all since my disk format was already converted info APFS. I kept using **_Command (⌘)-R_** since then.

You can show log window by **_Command (⌘)-L_** or at the menu bar. Make it show your all logs instead of only errors. It helps you identify your problem more precisely.


# Downloading Stuck
At this point your installation progress should be stopped for hours. When you check the last log it will probably say something like
`Retrying http://swcdn.apple.com/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/InstallESDDmg.pkg after 1 failure(s)`
The part `InstallESDDmg.pkg` may be different but you should see the pattern
`Retrying http://swcdn.apple.com/content/downloads/.../[filename] after # failure(s)`
Then this instructions may help you out from the problem.

Note that my solution is pretty complecated than it supposed to be considering the problem caused by a network issue. There might be some other solutions, but this is the only one that I found so far.

## Setup your environment
You need another PC. I used Ubuntu. Open terminal.

Clone this git repo.

```git clone```

Move to the folder.

```cd install-macos-high-sierra```

Install python requirements. I used python3.

```pip install -r requirements.txt```

Install DNSMasq.

```
sudo apt update
sudo apt install dnsmasq
```


## Pre-download the installation files
Now you need to pre-download and place it under right position.
You download them from `http://swcdn.apple.com`
But you will have to use `curl` to continue the downloading when it stops.

Example `curl -O -C - http://swcdn.apple.com/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/InstallESDDmg.pkg`
Monitor if the `current download speed` drops to 0. If that happens, cancel the process with `Ctrl + C` and rerun the command again. It will autometically continue downloading from where you ended.


### Essential files
| SIZE (B) | FILENAME |
| --- | --- |
| 2613171 | AppleDiagnostics.dmg |
| 490961728 | BaseSystem.dmg |
| 4668317536 | InstallESDDmg.pkg |

### Files I downloaded but the installer didn't used
| SIZE (B) | FILENAME |
| --- | --- |
| 10849613 | InstallAssistantAuto.pkg |
| 492474212 | RecoveryHDMetaDmg.pkg |

### All files used by the installer in order
```
/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/InstallInfo.plist
/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/OSInstall.mpkg
/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/AppleDiagnostics.dmg
/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/AppleDiagnostics.chunklist
/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/InstallESDDmg.pkg
/content/downloads/62/30/091-05077/8243xxpqrcv69hakbdhxdlw1iiffa9yi18/OSX_10_13_IncompatibleAppList.pkg
/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/BaseSystem.dmg
/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/BaseSystem.chunklist
```

As you can see, I skipped downloading few small files. It worked fine for me. But maybe not for your case. It's your choice.

### MD5 Checksum of some files I downloaded
| MD5 | Filename |
| --- | --- |
| e8d471a8807e3c9bae08e57018ac6aeb | AppleDiagnostics.dmg |
| 83b0c9aab879e7e4c1930f8a691bd8a4 | BaseSystem.dmg |
| 1fdf3ef7735a081648c589b933517c65 | InstallAssistantAuto.pkg |
| 7df5594a3a9830377147a48fc09edf9b | InstallESDDmg.pkg |
| 3b9d5ee01af925485c111375bbc576c8 | RecoveryHDMetaDmg.pkg |


Once you downloaded all files you need, place them in the exact same directory as its url under the `storage` folder.


## Setup your file server
Copy the configuration file then restart DNSMasq.

```
sudo cp swcdn.apple.com.conf /etc/dnsmasq.d/
sudo service restart dnsmasq
```

Start flask server

```
sudo python server.py
```

Now you're File server and DNS server is running.
You can test that by running

```
curl -O http://swcdn.apple.com/content/downloads/04/61/091-34298/almpfkbhyxnsgbxxqhoqo7sb40w3uip0wk/AppleDiagnostics.dmg
md5sum AppleDiagnostics.dmg
```

The download should've done in a second and the checksum must match with the original.

## Configure your iptime
Now you have to make your macbook connect to your DNS server. Since it's impossible to modify `/etc/hosts` or `/etc/resolv.config` in Recovery Mode, you'll have to find a way to configure your router. Change the DNS Server Setting of your router to use your DNS Server's IP address. You'll easily find a way to do this by searching from google.


## Retry installation in Recovery Mode
Now everything is setup. Restart your mac to boot in Recovery Mode if you haven't yet.
Retry reinstall macOS. It will work fine. After the reinstallation gets done, your system will get rebooted then it will continue the installation proccess.

If you see the same problem occuring at this step, check the log. Find out at which file you're stuck, download that file into your File server, close installer, restart installation again.



# Disk Password is Required
