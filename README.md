# Mail messages detection with Python
## Example of realization:

<img src="https://github.com/ArtemenkoDany/mailspam/blob/main/Photos/0.jpg" alt="image" width="50%"/>
<img src="https://github.com/ArtemenkoDany/mailspam/blob/main/Photos/1.jpg" alt="image" width="50%"/>
<img src="https://github.com/ArtemenkoDany/mailspam/blob/main/Photos/3.jpg" alt="image" width="50%"/>

## Used libraries:
### imaplib
To work with mail.
Here is documentation for imaplib: https://docs.python.org/3/library/imaplib.html

### grappa
grappa is a behavior-oriented, self-declarative, expressive and developer-friendly lightweight assertion library for Python that aims to make testing more productive and frictionless for humans.
grappa comes with two declarative assertion styles: ```expect``` and ```should```

## In code I use special dictionary which I called Dictlist.
It works like common dictionary, but here for one key could be array of parameters.
```
class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)
```

## Main idea
That code works like:
```
1. connect to mail
2. choose first 20 massages
3. check if date of mails are same with current date
4. check if there 10 mail from same sender
5. send to connected mail report of what was in mails (subject + body) 
    and count of letters and numbers in it
6. delete that 10 mails
```


<div align="center">
 <a href="https://www.instagram.com/danyderudenko/">
        <img src="https://github.com/ultralytics/yolov5/releases/download/v1.0/logo-social-instagram.png" width="3%"/>
    </a>
 
 <a href="https://github.com/ArtemenkoDany">
        <img src="https://github.com/ultralytics/yolov5/releases/download/v1.0/logo-social-github.png" width="3%"/>
    </a>
 
 <a href="https://www.facebook.com/dany.kreet/">
        <img src="https://github.com/ultralytics/yolov5/releases/download/v1.0/logo-social-facebook.png" width="3%"/>
    </a>
</div>
