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
    # polygon mumbai testnet
    network = "mumbai"

    # creating sdk instance
    sdk = ThirdwebSDK(network)

    # authorizing using private key
    PRIVATE_KEY = os.getenv('THIRD_WEB_PRIVATE_KEY')

    sdk = ThirdwebSDK.from_private_key(PRIVATE_KEY, network)

    # establishing contract
    contract = sdk.get_nft_collection("0x048Ab89691f7C3c74F38B595588808705c0a13F6")

    # NFT metadata to store
    metadata = NFTMetadataInput.from_json({
        "name": name,
        "description": (avatarUrl[0:5] + userEmail[0:5] + name[0:5]),
        "image": avatarUrl,
    })

    # minting address
    tx = contract.mint_to("0xD426Dd09102cb7cc92568eD3f538185fc537B8A5", metadata)
    receipt = tx.receipt
    token_id = tx.id
    nft = tx.data()


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

        uploadToBlockChain(
            userEmail=userData['email'],
            avatarUrl=userData['avatarUrl'],
            name=userData['userName']
        )

        user.save()
