from game.database.session import SessionLocal
from game.models.save import Save
from game.models.player import PlayerState

class Repository:
    def __init__(self):
        self.session = SessionLocal()
    
    
    def get_all_saves(self):
        return self.session.query(Save).all()
    
    def get_player_state(self, save_id):
        return self.session.get(PlayerState, save_id)

        
    def create_save(self, name):
        save = Save(name=name)
        self.session.add(save)
        self.session.flush()
        self.session.add(PlayerState(save_id=save.id))
        self.session.commit()
        return save
    
    def create_player_state(self, save_id):
        ps = PlayerState(save_id=save_id)
        self.session.add(ps)
        self.session.commit()
        return ps
    
    def update_player_state(self, save_id, x, y, hp, attack):
        ps = self.session.get(PlayerState, save_id)
        if ps:
            ps.x = x
            ps.y = y
            ps.hp = hp
            ps.attack = attack
            self.session.commit()

    def close(self):
        self.session.close()
        return