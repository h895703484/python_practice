from PIL import Image

head_image=Image.open('tx.jpg')
bdd_image=Image.open('11.png').convert('RGBA')
bg_img=Image.new("RGBA",(640,640),(255,255,255))
head=head_image.resize((600,600),Image.ANTIALIAS)
bg_img.paste(head,(20,20,620,620))
bdd_pendant=bdd_image.resize((300,300),Image.ANTIALIAS)
bdd_pendant_box=(20,100,320,400)
bg_img.paste(bdd_pendant,bdd_pendant_box,mask=bdd_pendant)
bg_img.save('head_with_pendant.png')