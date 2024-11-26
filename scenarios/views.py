from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Scenario, Message
from movies.models import Genre
from _lib.open_ai.utils import get_old_messages, get_full_messages, generate_completion
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message_from_request(request):
    user = request.user  # 헤더의 토큰을 통해 인증된 사용자
    message_type = request.query_params.get('messageType')
    
    if not message_type:
        return Response({"error": "messageType is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 요청 데이터 검증
    content = request.data.get("content", "")
    genre_pk = request.data.get("genreId")
    
    if message_type == 'first':
        time = request.data.get('time')
        space = request.data.get('space')
        if not all([time, space, genre_pk]):
            return Response({"error": "Missing required fields for 'first' messageType"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 장르 가져오기
        genre = Genre.objects.get(pk=genre_pk)
        if not genre:
            return Response({"error": "Invalid genre"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 시나리오 생성
        scenario = Scenario.objects.create(user=user, genre=genre)
        message_content = json.dumps({
          "time": time,
          "space": space,
          "genre": genre.name
        })
        message = Message.objects.create(
            scenario=scenario, 
            type='request', 
            message_type=message_type, 
            content=message_content
        )
    elif message_type == 'revise':
        scenario_id = request.data.get('scenarioId')
        if not scenario_id:
            return Response({"error": "scenarioId is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            scenario = Scenario.objects.get(id=scenario_id, user=user)
        except Scenario.DoesNotExist:
            return Response({"error": "Scenario not found"}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            scenario=scenario,
            type='request',
            message_type=message_type,
            content=content
        )
    else:
        scenario_id = request.data.get('scenarioId')
        if not scenario_id:
            return Response({"error": "scenarioId is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scenario = Scenario.objects.get(id=scenario_id, user=user)
        except Scenario.DoesNotExist:
            return Response({"error": "Scenario not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if message_type == 'line':
          content = "등장 인물들의 대표 대사를 추천해줘"
        elif message_type == 'detail':
          content = "시나리오 내 주요 사건을 더욱 상세하게 말해줘"
        
        message = Message.objects.create(
            scenario=scenario, 
            type='request', 
            message_type=message_type, 
            content=content
        )
    
    # 기존 대화 내용 가져오기
    old_messages = get_old_messages(scenario.messages.all())
    
    # OpenAI 메시지 포맷 생성
    full_messages = get_full_messages(message_type, old_messages, message.content)
    
    # OpenAI API 요청
    try:
        openai_response_content = generate_completion(full_messages)
    except Exception as e:
        return Response({"error": f"OpenAI API Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # 응답 저장
    response_message = Message.objects.create(
        scenario=scenario, 
        type='response', 
        message_type=message_type, 
        content=openai_response_content
    )
    
    # 클라이언트로 응답
    return Response(
        {
            "statusCode": 201,
            "type": message_type,
            "scenarioId": scenario.id,
            "data": {
                "content": openai_response_content,
                "messageId": response_message.id,
            }
        },
        status=status.HTTP_201_CREATED
    )
