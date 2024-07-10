# Obtener la IP pública usando el ID de la interfaz de red
TASK_ARN=$(aws ecs list-tasks --cluster fastapi-cluster --service-name fastapi-service --query 'taskArns[0]' --output text)
aws ecs describe-tasks --cluster fastapi-cluster --tasks $TASK_ARN --query 'tasks[0].attachments[0].details'
NETWORK_INTERFACE_ID=$(aws ecs describe-tasks --cluster fastapi-cluster --tasks $TASK_ARN --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' --output text)
aws ec2 describe-network-interfaces --network-interface-ids $NETWORK_INTERFACE_ID --query 'NetworkInterfaces[0].Association.PublicIp' --output text


# Actualizar docker 
docker build -t backend-btg .
aws ecs update-service --cluster fastapi-cluster --service fastapi-service --force-new-deployment