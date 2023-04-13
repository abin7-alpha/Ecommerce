from string import Template

from janaushadi import settings

user_verification_template = Template(
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
                                        <body align="left" style="color:black">Dear """ + '$user_name' + """ ,<br> <br> Welcome to """+ '$app_name' + """. Please click the link below to verify your email id.
                                            <br><a href='""" + '$domain_address' + """?token=""" + '$verification_token' + """' style="color:#21ce99" >Verify Email</a><br>
                                            <br>Regards,<br>
                                            Team """ + '$app_name' + """<br>
                                        </body>
                                </html>
                            """
                        )

user_available_stocks_notification = Template(
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
                                        <body align="left" style="color:black">Dear """ + '$user_name' + """ ,<br> <br> Welcome to """+ '$app_name' + """.
                                            <p>The stock is available for $commodity_name, please order before it becomes unavailable</>
                                            <br>Regards,<br>
                                            Team """ + '$app_name' + """<br>
                                        </body>
                                </html>
                            """
                        )

change_password_template = Template(
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
                                    <body align="left" style="color:black">Dear """ + "$user_name" + """ ,<br> <br> You have requested for a password change. Please click the link below if you requested it.
                                    <br><a href='""" + "$domain_address" + """?token=""" + '$verification_token' + """' style="color:#21ce99" >Reset Password</a><br>
                                    <br>Regards,<br>
                                    Team """ + "$app_name" + """<br>
								</body>
						    </html>
                        """
                    )

generated_otp_template = Template(
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
                                    <body align="left" style="color:black">Dear """ + "$user_name" + """ ,<br> <br> Your one time password for retailer edit. Do not share it with anybody
                                    <br><h2>""" + "$otp" + """</h2><br>
                                    <br>Regards,<br>
                                    Team """ + "$app_name" + """<br>
								</body>
						    </html>
                        """
                    )

generated_otp_retailer_admin_edit_template = Template(
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
                                    <body align="left" style="color:black">Dear """ + "$user_name" + """ ,<br> <br> Your one time password for retailer edit generated by """ + "$staff_name" + """(mahaveer staff). Do not share it with anybody other than the staff
                                    <br><h2>""" + "$otp" + """</h2><br>
                                    <br>Regards,<br>
                                    Team """ + "$app_name" + """<br>
								</body>
						    </html>
                        """
                    )

generated_otp_forgot_admin_template = Template(
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
                                    <body align="left" style="color:black">Dear """ + "$user_name" + """ ,<br> <br> Your one time password for Reset Password generated by """ + "$staff_name" +"""(mahaveer staff). Do not share it with anybody other than the staff
                                    <br><h2>""" + "$otp" + """</h2><br>
                                    <br>Regards,<br>
                                    Team """ + "$app_name" + """<br>
								</body>
						    </html>
                        """
                    )

generated_otp_forgot_template = Template(
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
                                    <body align="left" style="color:black">Dear """ + "$user_name" + """ ,<br> <br> Your one time password for Reset Password. Do not share it with anybody
                                    <br><h2>""" + "$otp" + """</h2><br>
                                    <br>Regards,<br>
                                    Team """ + "$app_name" + """<br>
								</body>
						    </html>
                        """
                    )

commodity_availability_sms_template = Template("""Namaste Dear """ + "$user_name" + """,Your requested commodity""" + "$commodity_name" + 
                                            """\nis available. Order now before it becomes unavailable""" + 
                                            """\nregards,""" + "$app_name")

generate_otp_msg_forgot_template = Template("""Namaste Dear """ + "$user_name" + """,Youre one time password for Reset Password""" + "$otp" + 
                                            """\nregards,""" + "$app_name")

generate_otp_msg_forgot_admin_template = Template("""Namaste Dear"""+ "$user_name" + """,Youre one time password for Reset Password""" + """generated by """ + "$staff_name" + """(mahaveer staff)""" + "$otp" + 
                                                  """\n do not share it with anybody other than the staff""" + """regards,""" + "$app_name")

generate_otp_msg_template = Template("""Namaste Dear """+ "$user_name" + """,Youre one time password for Retailer Edit""" + "$otp" + 
                                     """\nregards,""" + "$app_name")

generate_otp_msg_admin_template = Template("""Namaste Dear"""+ "$user_name" + """,You'r one time password for Retailer Edit""" + """generated by""" + "$staff_name" + """(mahaveer staff).""" + "$otp" + 
                                           """\nDo not share it with anybody other than the staff""" + """regards,""" + "$app_name")
