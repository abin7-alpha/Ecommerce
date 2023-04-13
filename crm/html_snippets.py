from string import Template

reply_sms = Template("$message\n"
                     + 'regards,' + '$app_name')

reply_email = Template(
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
                                    <body align="left" style="color:black">
                                    <h3>""" + "$message" + """ </h3>
                                    <br>Regards,<br>
                                    Team """ + "$app_name" + """<br>
								</body>
						    </html>
                        """
                    )
