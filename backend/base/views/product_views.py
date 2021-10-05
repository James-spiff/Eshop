from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.contrib.auth.models import User
from base.models import Product, Review
from base.serializers import ProductSerializer

from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword') #get's the keyword being passed from the searchbox

    if query == None:
        query = ''

    #by default query is '' so this returns all the products same as using "objects.all" to get all the products
    products = Product.objects.filter(name__icontains=query)    #this filters whatever is inside query and returns it to the user. The 'i' in icontains means the value isn't case sensitive

    #Adding the pagination
    page = request.query_params.get('page')
    paginator = Paginator(products, 5) #takes in the queryset which is products and the number of items that can be displayed on a page

    try:
        products = paginator.page(page) #does the pagination
    except PageNotAnInteger:
        products = paginator.page(1) #for when we haven't selected a page in the pagination request(or clicked the pagination buttons) so it defaults to the 1st page
    except EmptyPage:
        products = paginator.page(paginator.num_pages) #returns the last page if the user requests for an empty page

    if page == None:    #setting the default page
        page = 1 

    page = int(page)

    serializer = ProductSerializer(products, many=True) #many=True is set to True because we are expecting more than one data in the case of only one data it's set to False
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})  #paginator.num_pages get's the length of the pages 


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
        
    return Response(serializer.data)


#a view that get's the top rated products
@api_view(['GET'])
def getTopProducts(requests):
    # The code below get's the 1st 5 ratings that are greater than or equal to 4
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5] #__gte=4 means greater than or equal to 4. __gt=4 means greater than 4

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
     
    product = Product.objects.create(
        user = user,
        name = 'Sample Name',       #These are dummy data incase we leave some fields blank
        price = 0,
        countInStock = 0,
        category = 'Sample Category',
        description = ''
    )
    serializer = ProductSerializer(product, many=False)
        
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']

    product.save()

    serializer = ProductSerializer(product, many=False)
        
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
        
    return Response('Product Deleted')



@api_view(['POST'])
def uploadImage(request):
    data = request.data 
    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()
    
    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    data = request.data
    product = Product.objects.get(_id=pk)

    #if customer has already submitted a review
    alreadyExists = product.review_set.filter(user=user).exists()

    if alreadyExists:
        content = {'detail': 'Product alredy reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    #if customer has no rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    #Create review
    else:
        review = Review.objects.create(
            user = user,
            product = product,
            name = user.first_name,
            rating = data['rating'],
            comment = data['comment']
        )

        reviews = product.review_set.all() #get's all the reviews from a product
        product.numReviews = len(reviews) #count's the number of reviews
        
        total = 0
        for i in reviews:
            total += i.rating   #get's the total sum of ratings

        product.rating = total / len(reviews) #get's the average rating which will be displayed on the frontend 
        product.save()
        
        #review.save()

        return Response({'Review added'})
    
