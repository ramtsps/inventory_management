@echo off
setlocal enabledelayedexpansion

:: Create output folder
mkdir agri_images
cd agri_images

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
set url1=https://m.media-amazon.com/images/I/81xqOLamkVL._SX522_.jpg
set url2=https://5.imimg.com/data5/SELLER/Default/2024/5/419825843/ZG/JP/HJ/7691762/real-super-manju-seed-500x500.jpg
set url3=https://www.agriplexindia.com/cdn/shop/products/Multiplex-Baba_3.png?v=1691064974
set url4=https://m.media-amazon.com/images/I/31GFslQx8SL._AC_UF1000,1000_QL80_.jpg
set url5=https://images.meesho.com/images/products/61874349/fovda_512.webp
set url6=https://cdn.shopify.com/s/files/1/0722/2059/files/hariyali-08-file-5948.jpg?v=1737434028
set url7=https://5.imimg.com/data5/GL/DN/MY-3900352/net-for-crop-protection-500x500.png
set url8=https://m.media-amazon.com/images/I/81K2FMA9w8L.jpg
set url9=https://img.myipadbox.com/upload/store/product_l/SYA003766.jpg
set url10=https://5.imimg.com/data5/SELLER/Default/2022/5/MC/ID/GW/44902003/new-product-500x500.jpeg
set url11=https://cpimg.tistatic.com/6362313/b/4/16-ltr-electric-manual-2-in-1-knapsack-sprayer.jpg
set url12=https://m.media-amazon.com/images/I/61M8Kdjr7SS._AC_UF894,1000_QL80_.jpg
set url13=https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSl794NdFpn4ulV4fxe26x46C5R5dXu9xP0NQ&s
set url14=https://m.media-amazon.com/images/I/813IbLtMzqL.__AC_SX300_SY300_QL70_FMwebp_.jpg
set url15=https://mahadhan.co.in/wp-content/uploads/2019/01/Sugarcane-Special.png
set url16=https://m.media-amazon.com/images/I/21FvQ98DFHL._AC_SS450_.jpg
set url17=https://m.media-amazon.com/images/I/71BorEhpVsL.jpg
set url18=https://i.pinimg.com/736x/df/16/c2/df16c26f6669fb60043cdc222645c3de.jpg
set url19=https://greenmoonusa.com/images/product/5kgblocks3.webp
set url20=https://m.media-amazon.com/images/I/61RCEbTfoRL._AC_SS450_.jpg
set url21=https://th.bing.com/th/id/OIP.ytK9UNT0sClEvlHXcktgUgHaHa?rs=1&pid=ImgDetMain
set url22=https://blueandgreentomorrow.com/wp-content/uploads/2022/01/shutterstock_693787120-800x534.jpg
set url23=https://th.bing.com/th/id/OIP.fpm0Co8ta4KM7wjoVTlutAHaHa?rs=1&pid=ImgDetMain
set url24=https://shehrikisaan.com/wp-content/uploads/2023/05/Cow-Manure-1100-x-1100-px-with-shadow-and-white-background-1024x1024.jpg
set url25=https://thumbs.dreamstime.com/b/organic-paddy-seeds-unmilled-rice-wood-background-healthy-food-131361069.jpg
set url26=https://rukminim1.flixcart.com/image/416/416/kuipea80/drip-irrigation-kit/p/l/s/drip-irrigation-4mm-feederline-pipe-with-4mm-pin-connector-50-original-imag7mgtu2aqzrnn.jpeg?q=70
set url27=https://5.imimg.com/data5/SELLER/Default/2023/4/301002287/DI/JL/WT/151057280/agriculture-products-500x500.jpg

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
