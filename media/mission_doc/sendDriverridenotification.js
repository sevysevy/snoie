export const sendDriverridenotification= async (req, res, next) => {
        try {
			//use 5km
            const distance = 5;
            const unitValue = 1000;
            let userTripdetailsData= await userTripdetails.createData(
                {
                startDestination:req.body.startDestination,
                Date:req.body.Date,
                Time:req.body.Time,
                customer_notes:req.body.customer_notes,
                userId:req.body.userId,
                start_location:req.body.start_location,
                EndDestination:req.body.EndDestination,
                Distance_travelled:req.body.Distance_travelled,
                amount:req.body.amount,
                loyalty_points:req.body.loyalty_points,
                end_location:req.body.end_location,
                vehicleTypeId:req.body.vehicleTypeId
            })
            console.log("userTripdetailsData",userTripdetailsData)
            const userData = await UserVehicledetailsModel.aggregate([
            {
                $geoNear: {
                    near: {
                        type: 'Point',
                        coordinates: [req.body.start_location.coordinates[0], req.body.start_location.coordinates[1]]
                    },
                    
                    maxDistance: distance * unitValue, // distance in meters
                    distanceField: 'distance',
                    distanceMultiplier: 1 / unitValue
                }
            },
            {
                '$lookup': {
                  'from': 'users', 
                  'localField': 'userId', 
                  'foreignField': '_id', 
                  'pipeline': [
                    {
                      '$match': {
                        'is_online': true
                      }
                    }
                  ], 
                  'as': 'userData'
                }
              },
              {
                '$lookup': {
                  'from': 'vehicletypes', 
                  'localField': 'vehicleTypeId', 
                  'foreignField': '_id', 
                  'as': 'vehicleclan'
                }
              },
              {
                '$match': {
                  'vehicleclan': {
                    '$ne': []
                  }
                }
              }, 
              {
                '$unwind': {
                  'path': '$userData', 
                  'preserveNullAndEmptyArrays': true
                }
              },
                {
                    $sort: {
                        distance: 1
                    }
                },
            
            ]);
          
            var registrationTokenArray=[]
            console.log("userData.length",userData.length)
            if(userData.length == 0)
            {
                throw new Error("There are no drivers available around!!!")
            }
            var result = []
			//filter driver by vehicle clan
			var result = []
            for(let user of userData){
                const vehicleClan = user.vehicleclan
                for(let clan of vehicleClan){
                    if(req.body.vehicleTypeId == clan._id){
                        result.push(user)
                        registrationTokenArray.push(user.userData.deviceToken)
                        break
                    }
                }
            }
            const  registrationToken1 = registrationTokenArray
            console.log("registrationToken1",registrationToken1)
            var pushMessage = { //this may vary according to the message type (single recipient, multicast, topic, et cetera)
                registration_ids:registrationToken1,
                content_available: true,
                mutable_content: true,
                notification: {
                    title: "Ride Request",
                    body: `Some One Requested For Ride!!`,
                        "image":'https://media.istockphoto.com/id/1464547965/photo/worker-thinking-or-typing-on-laptop-in-cafe-coffee-shop-or-restaurant-on-startup-ideas-vision.jpg?s=2048x2048&w=is&k=20&c=GPnra0Yal9RbRzRv76auIFBG20ErmkyPFosa3jzEthY=',
                },
                data: {
                    "click_action": "FLUTTER_NOTIFICATION_CLICK",
                    "sound": "default", 
                    "type": "RIDE_INVITE",
                    "subType": "general",
                    "tripId": userTripdetailsData._id,
                    "screen": "screenA",
                },
                icon : 'https://media.istockphoto.com/id/1464547965/photo/worker-thinking-or-typing-on-laptop-in-cafe-coffee-shop-or-restaurant-on-startup-ideas-vision.jpg?s=2048x2048&w=is&k=20&c=GPnra0Yal9RbRzRv76auIFBG20ErmkyPFosa3jzEthY=',//Default Icon
                sound : 'default',
            };

            fcm.send(pushMessage, function(err, response){
                if (err) {
                    console.log("Something has gone wrong!",err);
                    return next(new BadRequestError(err))
                                // throw new Error(err)
                } else {
                    console.log("Successfully sent with response: ", response);
                    let dataObject = {
                        message: "Driver Ride Notification Sent Succesfully",
                    };
                    return handleResponse(res, dataObject);
                }
            });
           

        }
        catch (e) {
          logger.log(level.error, `Error: ${JSON.stringify(e)}`);
          if (e && e.message) return next(new BadRequestError(e.message));
          
          return next(new InternalServerError());
		}
        
}