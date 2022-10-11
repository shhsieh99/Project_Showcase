while true; do
    docker-compose exec mids \
        ab -n 10 -H "Host: user1.comcast.com" \
            http://localhost:5000/purchase_a_sword
    docker-compose exec mids \
        ab -n 10 -H "Host: user1.comcast.com" \
            http://localhost:5000/purchase_armor
    docker-compose exec mids \
        ab -n 10 -H "Host: user1.comcast.com" \
            http://localhost:5000/purchase_a_shield
    docker-compose exec mids \
        ab -n 10 -H "Host: user1.comcast.com" \
            http://localhost:5000/join_guild
    docker-compose exec mids \
        ab -n 10 -H "Host: user2.att.com" \
            http://localhost:5000/purchase_a_sword
    docker-compose exec mids \
        ab -n 10 -H "Host: user2.att.com" \
            http://localhost:5000/purchase_armor
    docker-compose exec mids \
        ab -n 10 -H "Host: user2.att.com" \
            http://localhost:5000/purchase_a_shield
    docker-compose exec mids \
        ab -n 10 -H "Host: user2.att.com" \
            http://localhost:5000/join_guild
    sleep 10
done