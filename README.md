# What is this script for
This script fetches documents in Red Hat product pages.
You can find a list of documents for Red Hat products in https://docs.redhat.com/
.
# How to use
To download all the documents of RHEL in PDF format:

```
$ ./fetch_rh_docs.py -u USERNAME --pdf https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/
```

USERNAME is your Red Hat Network / Customer Portal account.
You might be prompted to input password of the account when you try to download contents which require to login to Customer Portal.

Once you input your password, it is stored in Python Keyring fascility.
That is, the password would be stored in *Gnome Keyring* on Linux Desktop or *Keychain Access.app* on Mac OS X.

# Depends
* Python libraries: [lxml](http://lxml.de/), [keyring](https://pypi.python.org/pypi/keyring)
* HTML to PDF converter: [wkhtmltopdf](http://wkhtmltopdf.org)

# Tested Environments
* Mac OS X 10.10 Yosemite + Keychain Access.app
* Fedora 21 + Gnome Keyring
* RHEL7.0 + encrypted text

# Note
If you encounter `ValueError: Missing environment variable:GOOGLE_KEYRING_USER` error storing your password in Fedora,
try to create config file **$HOME/.local/share/python_keyring/keyringrc.cfg** and set **default-keyring** to Gnome Keyring in **backend** section like this:

```
$ cat ~/.local/share/python_keyring/keyringrc.cfg
[backend]
default-keyring=keyring.backends.Gnome.Keyring
```

Then the password should be stored in Gnome Keyring.
