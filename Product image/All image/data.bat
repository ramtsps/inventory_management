Wheat Flour 5kg
Ponni Boiled Rice 25kg
Toor Dal 1kg
Toor Dal 1kg
Wheat Flour 5kg
Refined Sunflower Oil 1L
Idli Rice 10kg
Urad Dal 1kg
Chana Dal 1kg
Moong Dal Yellow 1kg
Besan (Gram Flour) 1kg
Rock Salt 1kg
Cooking Soda 100g
Sugar 5kg
Tamarind 500g
Coconut Oil 1L
Green Gram Whole 1kg
Flattened Rice 1kg
Semolina (Rava) 1kg
Tea Powder 500g
Coffee Powder 250g
Jaggery 1kg
Tamarind Paste 250g
Groundnut Oil 1L
Red Chilli Whole 500g
Coriander Seeds 250g
Jeera (Cumin) Seeds 250g

@echo off
setlocal enabledelayedexpansion

rem Create a folder for the images
mkdir product_images
cd product_images

rem Define all URLs
set url1=https://5.imimg.com/data5/SELLER/Default/2021/7/EQ/AA/AY/6428050/5-kg-wheat-flour-1000x1000.jpeg
set url2=https://th.bing.com/th/id/OIP.u0fdqh3fVc24dejRAQDTqAHaKA?rs=1&pid=ImgDetMain
set url3=https://th.bing.com/th/id/OIP.B-IYceOJNpfwBwKxiQPBsQHaJs?rs=1&pid=ImgDetMain
set url4=https://th.bing.com/th/id/OIP.B-IYceOJNpfwBwKxiQPBsQHaJs?rs=1&pid=ImgDetMain
set url5=https://th.bing.com/th/id/OIP.VIEXPiYSim_jBf_eEcJAIwHaJQ?rs=1&pid=ImgDetMain
set url6=https://m.media-amazon.com/images/I/81QDsW0zGdL._SL1500_.jpg
set url7=https://spicesupermarket.co.uk/wp-content/uploads/2022/05/Idli-Rice.png
set url8=https://www.tatanutrikorner.com/cdn/shop/products/B01HBFSSUK.MAIN_1024x1024_bdb4a8cc-d19c-45b8-b711-0723d89a9de8.png?v=1617015159
set url9=https://th.bing.com/th/id/OIP.gXzn42bPR0BIcEMbFuKVFgHaHa?rs=1&pid=ImgDetMain
set url10=https://th.bing.com/th/id/OIP.Gj6l7ll1XvF0Ggaox7sH7wHaHa?rs=1&pid=ImgDetMain
set url11=https://ourshopkorea.com/191-large_default/rajdhani-besan-gram-flour-1kg-.jpg
set url12=https://th.bing.com/th/id/OIP.gHmLMLtGsNfzvKNB3wa_nAHaKK?rs=1&pid=ImgDetMain
set url13=https://m.media-amazon.com/images/I/61B7nF8zi+L._SL1000_.jpg
set url14=https://cfn-catalog-prod.tradeling.com/up/5fba0c6142480f001bed85d4/98387aeb5bbfc5ceea9f60f46f97ffd7.jpg
set url15=https://kiasumart.com/wp-content/uploads/2021/03/8906006720282_0252_1472538670974.jpg
set url16=https://www.bombayspices.ca/wp-content/uploads/2019/03/PARACHUTE-COCONUT-OIL.jpg
set url17=https://th.bing.com/th/id/OIP.kd96CFWu1cicnJD-y99ErgHaHa?rs=1&pid=ImgDetMain
set url18=https://m.media-amazon.com/images/I/51E3h68ycjL.jpg
set url19=https://www.bigtrolley.com.au/cdn/shop/products/Kitchen-Treasures-Roasted-Semolina-1Kg-1_1024x1024.webp?v=1695076780
set url20=https://m.media-amazon.com/images/I/717ePALRxWL._SL1200_.jpg
set url21=https://m.media-amazon.com/images/I/51slmk1A3iL._SL1000_.jpg
set url22=https://alankarfoods.com/wp-content/uploads/2021/10/IMG_2405-HERBAL-ORGANIC-JAGGERY.jpg
set url23=https://objectstorage.ap-mumbai-1.oraclecloud.com/n/softlogicbicloud/b/cdn/o/products/122506--01--1660234832.jpeg
set url24=https://kiasumart.com/wp-content/uploads/2020/09/Knife-Groundnut-Oil-1L.jpg
set url25=https://www.dnvfoods.com/wp-content/uploads/2022/05/DRY-R.CHILLI-1-1.jpg
set url26=https://th.bing.com/th/id/OIP.S-K-P5oXoWqHx4eGpeL9zAHaHa?rs=1&pid=ImgDetMain
set url27=https://m.media-amazon.com/images/I/71C-W0ouZ4L._SL1000_.jpg




set count=1
:loop
call set url=%%url%count%%%
if defined url (
    echo Downloading image !count!...
    curl -L -o image!count!.jpg "!url!"
    set /a count+=1
    goto loop
)

echo.
echo ✅ All 12 images downloaded to 'product_images' folder.
pause




