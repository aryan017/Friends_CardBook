from app import app, db
from flask import request, jsonify
from models import Friend

# Get All Friends

@app.route("/api/friends",methods=["GET"])
def get_friends():
    friends=Friend.query.all()  # Select * From Friends
    result=[friend.to_json() for friend in friends]
    return jsonify(result)

# Create a Friend

@app.route("/api/friends",methods=["POST"])
def create_friend():
    try: 
        data=request.json
        
        required_fields=["name","role","description","gender"]
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error" : f'Missing the Required Field please add it : {field}'}),400
            
        name=data.get("name")
        role=data.get("role")
        description=data.get("description")
        gender=data.get("gender")
        
        if gender=='male':
            img_url=f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender=='female':
            img_url=f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url=None
        
        new_Friend=Friend(name=name,role=role,description=description,gender=gender,img_url=img_url)
        
        db.session.add(new_Friend)
        
        db.session.commit()
        
        return jsonify(new_Friend.to_json()),201
    
    except Exception as e:
        db.session.rollback()
        
        return jsonify({"error" : str(e)}),500

# Delete a Friend

@app.route("/api/friends/<int:id>",methods=["DELETE"])
def delete_friend(id):
    try :
        friend=Friend.query.get(id)
        
        if friend is None : 
            return jsonify({"error" : "Friend Doesn't Exist"}),404
        
        db.session.delete(friend)
        db.session.commit()
        
        return jsonify({"msg" : "Friend Deleted Successfully"}),200
    except Exception as e :
        db.session.rollback()
        
        return jsonify({"error" : str(e)}), 500
    
# Update Friend Details

@app.route("/api/friends/<int : id>",methods=["PATCH"])
def update_friend(id):
    try:
        friend=Friend.query.get(id)
        data=request.json
        if friend is None : 
            return jsonify({"error" : "Friend Doesn't Exist is Database"}), 404
        
        friend.name=data.get("name",friend.name)
        friend.role=data.get("role",friend.role)
        friend.description=data.get("description",friend.description)
        friend.gender=data.get("gender",friend.gender)
       # friend.imag_url=f"https://avatar.iran.liara.run/public/{data.get("gender")}?username={data.get("name")}"
        
        db.session.commit()
        
        return jsonify({"msg" : "Friend Details Updated SuccessFully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : str(e)}),500