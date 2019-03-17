# -*- coding:utf-8 -*-

# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import csv
import json
import requests

# get API call with basic authentication
csvFile = open('sample.csv', 'r')

# read file section
dict_reader = csv.DictReader(csvFile)

# write file section
# need to write fieldheader first
with open('outputSample.csv', mode='w') as csv_write_file:
    fieldnames = ["id","merged_ids","currency_code","time_zone","star_rating","phone_number","content_updated_at","name","location_description","description","address","locality","region","postal_code","country_code","latitude","longitude","brand","chain","amenities","images","room_types"]
    writer = csv.DictWriter(csv_write_file, fieldnames=fieldnames)
    writer.writeheader()
    # for loop reader data content
    for row in dict_reader:
        # row["uuid"], this will be the parameter
        url = 'https://supply.integration2.testaroom.com/hotel/api/properties/%s.json?api_key=8ca4ce92-99ad-574c-b540-2c6308dd5570&auth_token=5ec5aa84-ac7a-5481-8823-94713f37816b/' % row["uuid"]
        user = "8ca4ce92-99ad-574c-b540-2c6308dd5570"
        passwd = "5ec5aa84-ac7a-5481-8823-94713f37816b"

        auth_values = (user, passwd)
        response = requests.get(url, auth=auth_values)
        data = response.json() # data is the json boby for content

        # brand's value somethines is null
        brand = ''
        if "brand" in data:
            if "en" in "brand":
                brand = data["brand"]["name"]["en"]
            else:
                brand = "NA"
        else:
            brand = "NA"

        # chain's value somethines is null
        chain = ''
        if "chain" in data:
            if "en" in "chain":
                chain = data["chain"]["name"]["en"]
            else:
                chain = "NA"
        else:
            chain = "NA"

        # region's value sometimes null
        region = ''
        if "region" in data:
            region = data["address"]["region"]["en"]
        else:
            region = "NA"

        # merged_ids
        newMerged_ids = ""
        if "merged_ids" in data:
            for i in data["merged_ids"]:
                newMerged_ids += i + "\n"

        # images sometimes empty
        images = ''
        if "images" in data:
            for i in data["images"]:
                images += "width: %s \n height: %s \n version: %s \n id: %s \n url: %s \n" % (str(i["width"]),str(i["height"]),str(i["version"]),i["id"],i["urls"]["large"])
        else:
            images = "NA"

        # amentities condition
        newAmentities = ""
        if "amenities" in data:
            for i in data["amenities"]:
                newAmentities += "id: %s \n name: %s \n" % (i["id"],i["name"]["en"])

        # room types condition        
        newRoomTypes = ""
        if "room_types" in data:
            for i in data["room_types"]:
                # room_types_name condition
                room_types_name = ''
                if "name" in i:
                    room_types_name = i["name"]["en"]
                else:
                    room_types_name = "NA"

                # room_types_description condition
                room_types_description = ""
                if "description" in i:
                    if "en" in "description":
                        room_types_description = i["description"]["en"]
                else:
                    room_types_description = "NA"

                # room type amenities condition    
                room_types_amenities = ""
                # if the room_types amenities are not empty
                if "amenities" in i:
                    for y in i["amenities"]:
                        room_types_amenities += "id: %s \n name: %s \n" % (y["id"],y["name"]["en"])
                else:
                    room_types_amenities = "NA"       
                
                # room type images condition
                room_types_images = ""
                # if the room_types amenities are not empty
                if "images" in i:
                    for y in i["images"]:
                        # width in this room type
                        if "width" in y:
                            room_types_images_width = str(y["width"])
                        else:
                            room_types_images_width = "NA"

                        # height in this room type
                        if "heigh" in y:
                            room_types_images_height = str(y["height"])
                        else:
                            room_types_images_height = "NA"

                        # version in this room type
                        if "version" in y:
                            room_types_images_version = str(y["version"])
                        else:
                            room_types_images_version = "NA"

                        # id in this room
                        if "id" in y:
                            room_types_images_id = y["id"]
                        else:
                            room_types_images_id = "NA"

                        # url in this room
                        if "url" in y:
                            room_types_images_url = y["urls"]["large"]
                        else:
                            room_types_images_url = "NA"

                        # add each element to room type images
                        room_types_images += "width: %s \n height: %s \n version: %s \n id: %s \n url: %s \n" %(room_types_images_width,room_types_images_height,room_types_images_version,room_types_images_id,room_types_images_url)                         
                else:
                    room_types_images = "NA"
                # each room type add each other       
                newRoomTypes += "id: %s \n name: %s \n description: %s \n amenities: %s \n images: %s \n" % (i["id"],room_types_name,room_types_description,room_types_amenities,room_types_images) 
        # write to new file when looping
        writer.writerow({
            "id":data["id"],
            "merged_ids":data["merged_ids"],
            "currency_code":data["currency_code"],
            "time_zone":data["time_zone"],
            "star_rating":data["star_rating"],
            "phone_number":data["phone_number"],
            "content_updated_at":data["content_updated_at"],
            "name":data["name"]["en"],
            "location_description":data["location_description"]["en"],
            "description":data["description"]["en"],
            "address":data["address"]["street_address"]["en"],
            "locality":data["address"]["locality"]["en"],
            "region":region,
            "postal_code":data["address"]["postal_code"],
            "country_code":data["address"]["country_code"],
            "latitude":data["address"]["latitude"],
            "longitude":data["address"]["longitude"],
            "brand":brand,
            "chain":chain,
            "amenities":newAmentities,
            "images":images,
            "room_types":newRoomTypes
        })
        print("Just processed id: " + data["id"])

csvFile.close()