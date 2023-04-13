from string import Template

confirm_order_template = Template(
        """
            <html>
                <head>
                    <style>
                    #header{
                        background-color:""" + '$primary_color' + """;
                        width: 100%;
                    }

                    .line {
                        font-weight: 200;
                    }
                    </style>
                </head>
                <body align="center">
                    <div align="left" style="float: left;">
                        <img style="width:700px; height:auto;" src='""" + '$logo_url' + """'/>
                    </div>
                    <div align="right">
                        
                        <p>Order Summary</p>
                        <p>"""+ '$company_billing_name' + """</p>
                        <p>Date:""" + '$order_time' + """</p>
                        <p>Invoice Number: """ + '$invoice_number' + """</p>
                        <p>""" + '$retailer_user_name' + """</p>
                        <p>""" + '$retailer_shop_name' + """</p>
                        
                        <p>""" + '$customer_add_on_details' + """</p>
                        <p>Gross Total : """ + '$total_cost' + """</p>
                    </div>
                    <div align="center" id="header" style="background-color:""" + '$primary_color' + """;color:white; padding:20px 0px 20px 0px;margin:0px">

                        
                    
                        
                    </div>
                    """ + '$order_items_table' + '$final_tax_content' + """
                
                    <table style="width:100%">
                    <tr style="border-top:1px solid black"><th align="left">Sub Total: <br><span style="font-weight:normal;"></span></th> <td> : </td> <td>Rs. """ + '$total_cost' + """</td></tr>
                    <tr style="border-top:1px solid black"><th align="left">Tax: <br><span style="font-weight:normal;"></span></th> <td> : </td> <td>Rs. """ + '$other_charges' + """</td></tr>
                    <tr style="border-top:1px solid black"><th align="left">Delivery Charges: <br><span style="font-weight:normal;"></span></th> <td> : </td> <td>Rs. """ + '$total_delivery_cost' + """</td></tr>
                    <hr>
                    <tr style="border-top:1px solid black"><th align="left">Gross Total: <br><span style="font-weight:normal;"></span></th> <td> : </td> <td>Rs. """ + '$final_cost' + """</td></tr>
                    <hr>

                    <tr style="background-color:""" + '$primary_color' + """;color:white;min-height:80px"><td colspan="10" align="center">
                        <h4>Thanks for ordering with """ + '$company_name' + """</h4>
                    <span style="font-size:18px;font-weight: 800;">""" + '$company_billing_name' + """</span>
                    <span style="font-size:18px">""" + '$company_address' + """</span></br>
                    <span style="font-size:20px; color:black">""" + '$company_url' + """</span>
                    </td></tr></table>
                </body>
            </html>
		"""
)

confirm_order_admin_template = Template(
        """
            <html>
                <head>
                    <style>
                    #header{
                        background-color:""" + '$primary_color' + """;
                        width: 100%;
                    }

                    .line {
                        font-weight: 200;
                    }
                    </style>
                </head>
                <body align="center">
                    <div align="left" style="float: left;">
                        <img style="width:450px; height:210px;" src='""" + '$logo_url' + """'/>
                    </div>
                    <div align="right">
                        
                        <p>Order Summary</p>
                        <p>"""+ '$company_billing_name' + """</p>
                        <p>Date:""" + '$order_time' + """</p>
                        <p>Invoice Number: """ + '$invoice_number' + """</p>
                        <p>""" + '$retailer_user_name' + """</p>
                        <p>""" + '$retailer_shop_name' + """</p>
                        
                        <p>""" + '$customer_add_on_details' + """</p>
                        <p>Gross Total : """ + '$total_cost' + """</p>
                    </div>
                    <div align="center" id="header" style="background-color:""" + '$primary_color' + """;color:white; padding:20px 0px 20px 0px;margin:0px">

                        
                    
                        
                    </div>
                    """ + '$order_items_table' + '$final_tax_content' + """
                
                    <table style="width:100%">
                    <tr style="border-top:1px solid black"><th align="left">Sub Total: <br><span style="font-weight:normal;"></span></th> <td> : </td> <td>Rs. """ + '$total_cost' + """</td></tr>
                    <hr>
                    <tr style="border-top:1px solid black"><th align="left">Gross Total: <br><span style="font-weight:normal;"></span></th> <td> : </td> <td>Rs. """ + '$final_cost' + """</td></tr>
                    <hr>

                    <tr style="background-color:""" + '$primary_color' + """;color:white;min-height:80px"><td colspan="10" align="center">
                        <h4>Thanks for ordering with """ + '$company_name' + """</h4>
                    <span style="font-size:18px;font-weight: 800;">""" + '$company_billing_name' + """</span>
                    <span style="font-size:18px">""" + '$company_address' + """</span></br>
                    <span style="font-size:20px;color:white">""" + '$company_url' + """</span>
                    </td></tr></table>
                </body>
            </html>
		"""
)

stock_availability_staff_notify_email = confirm_order_admin_template = Template(
        """
            <html>
                <head>
                    <style>
                    #header{
                        background-color:""" + '$primary_color' + """;
                        width: 100%;
                    }

                    .line {
                        font-weight: 200;
                    }
                    </style>
                </head>
                <body align="center">
                    <div align="center">
                        
                        <p>Stock of """+ '$commodity_name' + """\nis below the minimum stock benchmark :""" + '$minimum_available_quantity' +""" </p>
                        <p> Current available stock:"""+ '$available_quantity' +"""</p>
                    </div>
    
                    </div>
                </body>
            </html>
		"""
)

order_shipped_email_template = Template(
        """
            <html>
                <head>
                </head>
                <body align="center">
                    <div align="center">
                        <p>Namste """ + """ '$user_name' """ + """Your order, invoice no:"""+ '$order_no' + """\n has been shipped and will be arrived shortly""" + """</p>
                        <p>""" + '$note' + """</p>
                    </div>
    
                    </div>
                </body>
            </html>
		"""
)

order_canceled_email_template = Template(
        """
            <html>
                <head>
                </head>
                <body align="center">
                    <div align="center">
                        <p>Namste """ + """ '$user_name' """ + """Your order, invoice no:"""+ '$order_no' + """\n has been canceled.""" + """</p>
                        <p>""" + '$note' + """</p>
                    </div>
    
                    </div>
                </body>
            </html>
		"""
)

order_delivered_email_template = Template(
        """
            <html>
                <head>
                </head>
                <body align="center">
                    <div align="center">
                        <p>Namste """ + """ '$user_name' """ + """Your order, invoice no:"""+ '$order_no' + """\n has been delivered""" + """</p>
                    </div>
                    </div>
                </body>
            </html>
		"""
)

generated_otp_retailer_order_admin_edit_template = Template(
                        """
                            <html>
				                <head>
					                <style>
                                        body{
                                            background-color:white;
                                            width: 100%;
                                            float:left;
                                            text-align:left;
                                            color:black;
                                        }
						            </style>
							    </head>
                                    <body align="left" style="color:black">Dear """ + "$user_name" + """ ,<br> <br> Your one time password for retailer order edit generated by """ + "$staff_name" + """(mahaveer staff). Do not share it with anybody other than the staff
                                    <h3>Order No: """ + "$order_no" + """ </h3>
                                    <br><h2>""" + "$otp" + """</h2><br>
                                    <br>Regards,<br>
                                    Team """ + "$app_name" + """<br>
								</body>
						    </html>
                        """
                    )

generate_otp_msg_retailer_order_edit_admin_template = Template("""Namaste Dear"""+ "$user_name" + """,You'r one time password for Retailer Order edit""" + """generated by""" + "$staff_name" + """(mahaveer staff).""" + "$otp" + '$order_no' +
                                           """\nDo not share it with anybody other than the staff""" + """regards,""" + "$app_name")

order_msg_template = Template("Namaste Dear "+ '$user_name' +", Your Order (id: " + '$order_id' + ") will be delivered without any shortage.\n Total Order Items : " +
                             '$total_order_items' + ". TotalAmount : Rs."+ '$total_amount' 
                              +"/-. Please check the app for all order details.\n" + "invoice:- $invoice \n"
                              + 'regards,' + '$app_name')

order_msg_verfied_template = Template("Namaste Dear "+ '$user_name' +", Your Order invoice no: " + '$order_id' + " has been verified by the admin and will be delivered without any shortage.\n Total Order Items : " +
                             '$total_order_items' + ". TotalAmount : Rs."+ '$total_amount' 
                              +"/-. Please check the app for all order details.\n" + "invoice:- $invoice \n"
                              + 'regards,' + '$app_name')

updated_order_msg_template = Template("Namaste Dear "+ '$user_name' +", Your Order (id: " + '$order_id' + ") has been updated by the admin and will be delivered without any shortage.\n Total Order Items : " +
                             '$total_order_items' + ". TotalAmount : Rs."+ '$total_amount' 
                              +"/-. Please check the app for all order details.\n" + "invoice:- $invoice \n"
                              + 'regards,' + '$app_name')

order_shipped_sms_template = Template("Namaste Dear "+ '$user_name' +", Your Order, invoice no: " + '$order_no' + " has been shipped and will be delivered shortly.\n" +
                             '$note')

order_canceled_sms_template = Template("Namaste Dear "+ '$user_name' +", Your Order, invoice no: " + '$order_no' + " has been canceled.\n" +
                             '$note')

order_delivered_sms_template = Template("Namaste Dear "+ '$user_name' +", Your Order, invoice no: " + '$order_no' + " has been delivered.\n")
