@echo off
setlocal enabledelayedexpansion

:: Create output folder
mkdir grocery_images
cd grocery_images

:: Product name list
set name1=Wheat_Flour_5kg.jpg
set name2=Ponni_Boiled_Rice_25kg.jpg
set name3=Toor_Dal_1kg_A.jpg
set name4=Toor_Dal_1kg_B.jpg
set name5=Wheat_Flour_5kg_B.jpg
set name6=Refined_Sunflower_Oil_1L.jpg
set name7=Idli_Rice_10kg.jpg
set name8=Urad_Dal_1kg.jpg
set name9=Chana_Dal_1kg.jpg
set name10=Moong_Dal_Yellow_1kg.jpg
set name11=Besan_Gram_Flour_1kg.jpg
set name12=Rock_Salt_1kg.jpg
set name13=Cooking_Soda_100g.jpg
set name14=Sugar_5kg.jpg
set name15=Tamarind_500g.jpg
set name16=Coconut_Oil_1L.jpg
set name17=Green_Gram_Whole_1kg.jpg
set name18=Flattened_Rice_1kg.jpg
set name19=Semolina_Rava_1kg.jpg
set name20=Tea_Powder_500g.jpg
set name21=Coffee_Powder_250g.jpg
set name22=Jaggery_1kg.jpg
set name23=Tamarind_Paste_250g.jpg
set name24=Groundnut_Oil_1L.jpg
set name25=Red_Chilli_Whole_500g.jpg
set name26=Coriander_Seeds_250g.jpg
set name27=Jeera_Cumin_Seeds_250g.jpg

:: Image URL list
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



:: Download and rename images
for /L %%i in (1,1,27) do (
    call set "link=!url%%i!"
    call set "newname=!name%%i!"
    echo Downloading image %%i ...
    curl -L -o "!newname!" "!link!"
)

echo.
echo ✅ All 27 images downloaded and renamed as per product names.
pause
