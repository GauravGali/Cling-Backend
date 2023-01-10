# Imports
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User
from .serializer import UserSerializer

from thirdweb import ThirdwebSDK
from thirdweb.types.nft import NFTMetadataInput

from dotenv import load_dotenv
import os

load_dotenv()

# Views
@api_view(['GET'])
def getRoutes(request):
    routes = {
        'Get All Users': {
            'Endpoint': '/users',
            'Method': 'GET',
            'Description': 'To Get All Users'
        },
        'Get Particular User': {
            'Endpoint': '/users/<user_id>',
            'Method': 'GET',
            'Description': 'To Get User With ID <user_id>'
        },
        'Create User': {
            'Endpoint': '/users/create',
            'Method': 'POST',
            'Description': 'To Create A User'
        }
    }

    return Response(routes)


@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUser(request, user_id):
    users = User.objects.get(id=user_id)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)

def uploadToBlockChain(userEmail, avatarUrl, name):
    # Support Network URL
    network = "mumbai"

    # Instance of the SDK
    sdk = ThirdwebSDK(network)

    PRIVATE_KEY = os.getenv("THIRD_WEB_PRIVATE_KEY")
    sdk = ThirdwebSDK.from_private_key(PRIVATE_KEY, network)

    contract = sdk.get_nft_collection("0x89252Cd13EaF48B92EFa921C40eAaCE3ade0eEdB")

    # Metadata
    metadata = NFTMetadataInput.from_json({
        "name": name,
        "description": userEmail[0:5]+avatarUrl[5:10]+name,
        "image": avatarUrl,
    })

    # Minting As NFT To Address
    tx = contract.mint_to("0xD426Dd09102cb7cc92568eD3f538185fc537B8A5", metadata)
    receipt = tx.receipt
    token_id = tx.id
    nft = tx.data()

    return


@api_view(['POST'])
def createUser(request):
    userData = request.data

    try:
        storedUrl = User.objects.get(email=userData['email'])

    except:
        user = User.objects.create(
            email=userData['email'],
            avatarUrl=userData['avatarUrl'],
            name=userData['userName']
        )
        user.save()

        uploadToBlockChain(
            userEmail=userData['email'],
            avatarUrl=userData['avatarUrl'],
            name=userData['userName']
        )



