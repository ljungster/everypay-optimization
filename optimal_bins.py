#! /usr/bin/python3

import csv

dictionary = {}
def set_up_dictionary():
    ## NOTE: MUST CHANGE FILE
    with open("Sample.csv", mode = "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            #variables that we import from the sheet
            amount = int(row["amount"])
            status_id = int(row["status_id"])
            country = row["country"]
            funding_type = row["funding_type"]
            card_level = row["card_level"]
            bin_number = row["bin_number"]
            issuer = row["issuer"]
            class_type = row["class_type"]

            #creating our array of values. ## NOTE: See above for index reference
            #if the dicitonary entry already exists (a previoue entry had the same bin)
            if dictionary.get(bin_number) != None:
                binArray = dictionary.get(bin_number)
                #increase the total amount
                binArray[8] += amount
            else:
                #create a new dictionary entry with the below values, the first
                #four entries refer to the status_id for the two class_type
                binArray = [0] * 9
                binArray[4] = country
                binArray[5] = funding_type
                binArray[6] = card_level
                binArray[7] = issuer
                binArray[8] = amount
            #if the class_type is alphabank
            if class_type == "alphabank":
                #if the transaction failed
                if status_id == 4:
                    binArray[1] += 1
                #for any other transaction status_id
                else:
                    binArray[0] += 1

            #if the class_type is nbg
            if class_type == "nbg":
                #if the transaction failed
                if status_id == 4:
                    binArray[3] += 1
                #for any other transaction status_id
                else:
                    binArray[2] += 1
            #updating our value in the dictionary
            dictionary[bin_number] = binArray
        return dictionary

def set_up_bin_sheet():
    #using the helper method declared above to create our file
    dictionary = set_up_dictionary()
    #writing the file with a csv writer, our CSV will have the following "headers"
    with open("optimal_bins.csv", mode = "w") as bin_file:
        fieldnames = ["bin_number", "total_amount", "average_amount", "country",
        "funding_type", "card_level", "issuer", "alpha_no", "alpha_other",
        "alpha_total", "alpha_fail_rate", "nbg_no", "nbg_other", "nbg_total",
        "nbg_fail_rate", "recommended_gateway"]

        #actually writing the file
        writer = csv.DictWriter(bin_file, fieldnames=fieldnames)
        writer.writeheader()
        #looping through every bin number in our dictionary
        for i in dictionary:
            #getting and creating the values that we need
            bin_number = i
            alpha_no = dictionary[i][1]
            alpha_other = dictionary[i][0]
            alpha_total = alpha_no + alpha_other
            nbg_no = dictionary[i][3]
            nbg_other = dictionary[i][2]
            nbg_total = nbg_no + nbg_other
            country = dictionary[i][4]
            funding_type = dictionary[i][5]
            card_level = dictionary[i][6]
            issuer = dictionary[i][7]
            total_amount = dictionary[i][8]
            average_amount = total_amount / (alpha_total + nbg_total)

            #calculating alphabank fail rates, None if there are less than 30 transactions
            alpha_fail_rate = None
            if alpha_total > 30:
                alpha_fail_rate = alpha_no / alpha_total

            #calculating nbg fail rates, None if there are less than 30 transactions
            nbg_fail_rate = None
            if nbg_total > 30:
                nbg_fail_rate = nbg_no / nbg_total

            #finding the best rate. # NOTE: Both alpha and nbg must have at least 30 transactions
            recommended_gateway = None
            #default is alphabank
            if alpha_fail_rate != None and nbg_fail_rate != None:
                best_rate = alpha_fail_rate
                recommended_gateway = "alphabank"
                #but if nbg is a lower fail rate, set it as the recommended_gateway
                if nbg_fail_rate < best_rate:
                    best_rate = nbg_fail_rate
                    recommended_gateway = "nbg"

            #We only write to our file if both alpha and nbg each have more than
            #30 transcations. Feel free to simply delete whichever parameters you
            #do not find useful. Be careful with commas, though.
            if recommended_gateway != None:
                #writing our csv file
                writer.writerow({"bin_number": bin_number, "total_amount": total_amount,
                "average_amount": average_amount, "country": country,
                "funding_type": funding_type, "card_level": card_level,
                "issuer": issuer, "alpha_no": alpha_no,
                "alpha_other": alpha_other, "alpha_total": alpha_total,
                "alpha_fail_rate": alpha_fail_rate, "nbg_no": nbg_no,
                "nbg_other": nbg_other, "nbg_total": nbg_total,
                "nbg_fail_rate": nbg_fail_rate,
                "recommended_gateway": recommended_gateway})
#running our function
set_up_bin_sheet()
