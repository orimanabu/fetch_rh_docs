# What is this script for
This script fetches documents in Red Hat product pages.
You can find a list of documents for Red Hat products in https://docs.redhat.com/
.

In this README, "https://docs.redhat.com/", which includes links to all products documents, is called *Product index*.
Pages linked from Product index, for example "https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/", are called *Product page*.

<!-- #_ -->

# How to use

## Basic use case #1
To download all PDF documents of all products, "--all-products" options is useful.

```
$ ./fetch_rh_docs.py -u USERNAME --all-products --pdf
```

Some contents require to login to Red Hat Network / Customer Portal.
You will be prompted to input user name and password of your Customer Portal account when you try to get the contents.
You can also pass your Customer Portal account name with "-u USERNAME" command line option.

Once you input your password, it is stored in Python Keyring fascility.
That is, the password would be stored in *Gnome Keyring* on Linux Desktop or *Keychain Service* on Mac OS X.

## Basic use case #2
To download all PDF documents of a products, append URL of product page to the end of the command.
For example for RHEL,

```
$ ./fetch_rh_docs.py -u USERNAME --pdf https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/
```

## Only listing URLs
If you don't want to download documents actually but only want to know the URL list of PDF files, add "--list" option.

```
$ ./fetch_rh_docs.py -u USERNAME --pdf --list https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/
```

## Getting Knowledge Base
Some products have links to Knowledge Base in their product page. If you get URLs of the KB, use "--kb" option.

```
$ ./fetch_rh_docs.py -u USERNAME --kb --list https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/
```

You can use "--pdf" and "--kb" simultaneously.

```
$ ./fetch_rh_docs.py -u USERNAME --pdf --kb --list https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/
```

## URL filtering
If you filter URLs with regular expressions, use "--includes *REGEXP*" and/or "--excludes *REGEXP*" option. You can add these options multiple times.

E.g. To get 'Cluster' related manuals of RHEL5 but want to exclude 'Oracle' related ones, run the script like this:

```
$ ./fetch_rh_docs.py -u USERNAME --pdf --includes '\/5\/' --includes 'Cluster' --excludes 'Oracle' https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/
```

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
