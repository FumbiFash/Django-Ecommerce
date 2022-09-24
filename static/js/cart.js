
var updatebtns = document.getElementsByClassName('update-cart')

// create/add event handler for each button 
for(i = 0; i < updatebtns.length; i++){
        updatebtns[i].addEventListener('click',function(){
            var productId = this.dataset.product
            var action = this.dataset.action
            console.log("productId: ",productId,'Action: ', action)


            

            if(user == 'AnonymousUser'){

                addCookieItem(productId,action)
                
            }   
            
            else{
                
                updateUserOrder(productId,action)
                
            }
            
        })

       
}


function addCookieItem(productId,action){
    console.log('iii')

    if(action == 'add'){
        if(cart[productId] == undefined ){

            cart[productId] = {'quantity' : 1}
            
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0 ){
            
            delete cart[productId] 
            
        }    
    }

    document.cookie = 'cart=' + JSON.stringify(cart) +';domain=;path=/'


    location.reload()



}

function updateUserOrder(productId,action){
    console.log("user is authenticated, sending data....")

    let url = '/update_item'

    fetch(url,{

        method:'POST',

        headers:{

            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken

        },
        
        //information being sent to backend
        body: JSON.stringify({
            'productId':productId,'action':action
        })
    })
    .then((response)=> {
        return response.json()
    })
    .then((data)=>{
        console.log("data :",data)
        
        //reload page on each click
        location.reload()
    })

}

var removeall = document.getElementsByClassName('removeall')
		

			for(i = 0;i<removeall.length;i++){
				console.log("dwak")

				removeall[i].addEventListener('click',function(){
                    var productId = this.dataset.product
                    var action = this.dataset.action
                    console.log("productId: ",productId,'Action: ', action)
                
					// delete cart[productId]
					
					
				if (user == 'AnonymousUser'){

                    
            
                    delete cart[productId] 
                    
                    document.cookie = 'cart=' + JSON.stringify(cart) +';domain=;path=/'


                    location.reload()
                            

                }

                else{

                    updateUserOrder(productId,action)



                }
			})
			
			
		}
