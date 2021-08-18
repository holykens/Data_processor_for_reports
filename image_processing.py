from PIL import Image
import Input

with open(Input.parameters_for_cropping_filepath) as myfile:     #open files processing image input
    #csv_reader=csv.reader(myfile,delimiter=",")
    lines=myfile.readlines()                            #get the content of file

strip_lines=[]                                          #Assign strip_lines as a blank list
for line in lines:                                      #loop for each line in the file content
    line=line.strip()                                   #strip the \n
    strip_lines.append(line)                            #append line to strip_lines list

graphs_name_list = []                                   #Assign graphs_name_list as a blank list

for line in strip_lines:                                #loop for processing images
    line_list = line.split(",")                         #assign line_list as list of items in line string after splitting line identifier
    for x in range(int(line_list[1])):                  #loop for duplicated images processing
        if int(line_list[1]) != 1:                      #Conditional for cropping image for more than 1 time
            graph_name_after_cropping = line_list[2] + line_list[x+3+x*4] + "_cropped.png"      #Assign identifier for output image name
            left = int(line_list[x+4+x*4])               #Assign identifier for x argument in cropping method
            top = int(line_list[x+5+x*4])                #Assign indentifier for y argument in cropping method
            right = int(line_list[x+6+x*4])             #Assign identifier for width argument in cropping method
            bottom = int(line_list[x+7+x*4])            #Assign identifier for height argument in cropping method
            graphs_name_list.append(graph_name_after_cropping)
        else:                                               #Conditional for cropping image 1 time
            graph_name_after_cropping = line_list[2] + "_cropped.png"       #Assign identifier for output image name
            left = int(line_list[x+4+x*4])                  #Assign identifier for x argument in cropping method
            top = int(line_list[x+5+x*4])                   #Assign indentifier for y argument in cropping method
            right = int(line_list[x+6+x*4])                  #Assign identifier for width argument in cropping method
            bottom = int(line_list[x+7+x*4])                #Assign identifier for height argument in cropping method
            graphs_name_list.append(graph_name_after_cropping)

        im = Image.open('images_before_cropping\\%s.png' % line_list[2]).convert('RGB')     #open the raw image in color mode
        im = im.crop((left, top, right, bottom))         #Crop the image
        im.save('images_after_cropping\\%s' % graph_name_after_cropping)        #save the cropped image

