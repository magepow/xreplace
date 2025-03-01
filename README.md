[<img src="https://github.com/magepow/themeforest/blob/master/shopify/shopify_affiliate.jpg" >](https://shopify.pxf.io/VyL446)

# xreplace
## Xreplace Tools find and replace many content by Magepow

## ✓ Install Xreplace via git (recommend)
Login with root user and run commands:

```
Requirement
pip3 install xlrd==1.2.0
pip3 install pandas
pip3 install openpyxl
pip3 install python-dotenv


cd ~
git clone https://github.com/magepow/xreplace.git
cd xreplace
ln -s `pwd`/xreplace.py /usr/bin/xreplace
cp .env.sample .env
xreplace
```
*Usage:

    Add content need find and replace in file xreplace.xlsx
  
    Col "Find" content need find
  
    Col "Replace" replace content in "Find"
  
note: You can change file and extension file find and replace in file .env

*Commands
  ```
      # Use default file xreplace.xlsx
      xreplace
      # Or special path file
      xreplace ./xreplace_8.xlsx
      # Or use via magento choose option 16 and enter path file
  ```
