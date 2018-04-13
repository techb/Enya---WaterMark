import Enya

e =  Enya.Enya()

wimg = e.getWatermkImage("C:\\Users\\KB\\Dev\\WaterMarkGUI\\watermarktest.png")

d = e.getImgDir("C:\\Users\\KB\\Dev\\WaterMarkGUI\\samples_copy")

e.watermark(wimg, d)