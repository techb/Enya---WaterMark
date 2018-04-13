# sudo easy_install pip3
# sudo -H pip3 install Pillow

from PIL import Image
import os

class Enya:

    def __init__(self):
        self.checkpos = []

    def markit(self, img, wimg):
        """ This is where the actual watermarking happens. Note the use of eval() for the position
        is VERY bad idea and should NOT be done this way, yet here we are lol. """
        print(img.split("/")[-1])
        photo = Image.open(img)
        pwidth, pheight = photo.size
        wwidth, wheight = wimg[1]

        for key in self.checkpos:
            try:
                if self.checkpos[key][0] == "1":
                    photo.paste(wimg[0], eval(self.checkpos[key][1]), mask=wimg[0])
            except:
                pass
        
        # save in new folder so to keep the origial copy untouched
        photo.save(self.copypath+"/"+img.split("/")[-1])
        photo.close()
    

    def getWatermkImage(self, imgpath):
        """ opens the image from the supplied path that's used as the watermark.
        returns tuple - 0 is image object, 1 is tuple containing px size x,y """
        wimg = Image.open(imgpath)
        wimg = (wimg, (wimg.size))
        return wimg
        
    def getImgDir(self, thedir):
        """ walk dir of images to be watermarked and return list of them """
        dirlist = []
        for i in self.absoluteFilePathsRecursive(thedir):
            dirlist.append(i)
        return dirlist
        
    def absoluteFilePathsRecursive(self, directory):
        """ This is recursive and will walk all child folders """
        for dirpath,_,filenames in os.walk(directory):
            for f in filenames:
                yield os.path.abspath(os.path.join(dirpath, f))

    def watermark(self, watermark, dlist, loghandle=None, proghandle=None, checkboxes=None, strthandle=None, guihandle=None):
        ''' This needs refactored to not use handles to the gui. Honestly, this whole project should
        be refactored lol. '''
        watermark = self.getWatermkImage(watermark)
        self.copypath = dlist
        self.copypath += "_watermark"

        # make dir to hold new watermarked images
        if (not os.path.isdir(self.copypath)):
        	os.mkdir(self.copypath)

        dlist = self.getImgDir(dlist)
        self.checkpos = checkboxes

        # set length of progress bar
        proghandle["maximum"] = len(dlist)

        # disable the 'start' button so user doesn't spam new threads and wreck it
        strthandle.config(state="disabled")
        for i in dlist:
            # ugly try/except, but at least handles files that aren't images
            try:
                self.markit(i, watermark)
                if loghandle and guihandle:
                    lmessage = "Watermarking %s..." % i.split("/")[-1]
                    loghandle.insert('end', lmessage+"\n")
                    loghandle.see('end')

            except:
                print("Can't open %s, skipping" % i)
                continue

            proghandle["value"] += 1

        watermark[0].close()
            
        proghandle["value"] = proghandle["maximum"]
        loghandle.insert('end', "\nAll Done!\n")
        loghandle.see('end')
        # enable 'start' button again
        strthandle.config(state="normal")