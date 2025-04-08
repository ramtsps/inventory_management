@echo off
setlocal enabledelayedexpansion

:: Create a folder for the images
mkdir agri_images
cd agri_images

:: Define all URLs
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
set url27=https://5.imimg.com/data5/SELLER/Default/2023/4/301002287/DI/JJ/NI/29610149/neem-cake-fertilizer-1000x1000.jpeg
set url28=https://th.bing.com/th/id/OIP.A6cyQBJKR1LpX6NL5nj56wHaHC?rs=1&pid=ImgDetMain
set url29=https://th.bing.com/th/id/OIP.KMUM0N1qtp6Cr9wx4_3DWAHaHa?rs=1&pid=ImgDetMain
set url30=https://5.imimg.com/data5/SELLER/Default/2023/4/299641927/WY/MX/RW/16413710/vermicompost-50-kg-pack-500x500.jpg
set url31=https://m.media-amazon.com/images/I/510-UFtJavL._AC_.jpg
set url32=https://1.bp.blogspot.com/-BN_5As4QQOU/YQd0jvniDsI/AAAAAAAAC1o/cVWYrJTZJWo5YwbM6So3Sam5Bc2V9EAagCLcBGAsYHQ/s1500/61dU-Mlu0CL._SL1500_.jpg
set url33=https://cdn.shopify.com/s/files/1/0120/9853/5483/products/drmeter_soil_meter_3_in_1_1200x1200.jpg?v=1567565592
set url34=https://rukminim2.flixcart.com/image/416/416/xif0q/plant-seed/n/b/i/500-turmeric-seed-rhizome-variety-prathibha-na-keralagro-original-imagzcgnap9azgcg.jpeg?q=70
set url35=https://www.kisanshop.in/s/65f83b39d13b931b1c1f1a9b/667cf7ede166970024c66ccc/sarpan-green-long-101-brinjal-seeds-640x640.jpg
set url36=https://m.media-amazon.com/images/I/61DiUKCOmfL._SX300_SY300_QL70_ML2_.jpg
set url37=https://www.directfarmsupplies.co.uk/prototype/wp-content/uploads/2015/12/341316.jpg
set url38=https://i0.wp.com/www.droneassemble.com/wp-content/uploads/2016/03/1-4.jpg?resize=1000%2C1000
set url39=https://ms-profiles.objectstore.e2enetworks.net/479428-3XU-sprouted-pouch-sample-5.jpg

:: Download loop
set count=1
:loop
call set "url=%%url!count!%%"
if defined url (
    echo 🔽 Downloading image !count!...
    curl -L -o image!count!.jpg "!url!"
    set /a count+=1
    goto loop
)

echo.
echo ✅ All images downloaded to 'agri_images' folder.
pause
