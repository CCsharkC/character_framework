from random import uniform

class Entity():

    def __init__(self, **kwargs):

        self.mood_stats = {'Mood': None}
        """
        Changable Stats,
        Current supported mood stats:

        Mood: Sad > 0 - 100 < Happy
        """

        self.personality_stats = {'Social': None,
                                  'World': None,
                                  'Information': None,
                                  'Decision': None}
        """
        Constant Stats
        Current supported personality stats:

        Social: Introvert > 0 - 100 < Extrovert
        World: Perceptive > 0 - 100 < Judgmental
        Information: Sensing > 0 - 100 < Intuition
        Decision: Thinking > 0 - 100 < Feeling
        """
        self.statlets = {}
        self.statlets_decay = {}

        for stat in kwargs.items():
            if stat[0] in self.mood_stats:
                self.mood_stats[stat[0]] = stat[1]
            elif stat[0] in self.personality_stats:
                self.personality_stats[stat[0]] = stat[1]

    def apply_statlets(self):
        """
        Updates the mood and personality statistics of the object based on the provided statlets.
        """
        garbage_statlets = set()
        # Update mood and personality stats
        for stat_name, stat_value in self.statlets.items():
            if stat_name in self.mood_stats:
                if 0 <= self.mood_stats[stat_name] + stat_value <= 100:
                    self.mood_stats[stat_name] += stat_value

        # Update statlets and remove any that have decayed to zero
        for statlet_name in self.statlets_decay:
            if statlet_name in self.statlets:
                total = self.statlets[statlet_name] + self.decay_roll(decay_name=statlet_name)

                if (self.statlets[statlet_name] == 0 or
                        self.statlets[statlet_name] < 0 < total or
                        self.statlets[statlet_name] > 0 > total):
                    garbage_statlets.add(statlet_name)
                else:
                    self.statlets[statlet_name] = total

        # Remove any statlets that have decayed to zero
        for statlet_name in garbage_statlets:
            del self.statlets[statlet_name]
            del self.statlets_decay[statlet_name]

    def decay_roll(self, *, decay_name: str) -> int:
        """
        Calculate the decay roll for a given decay.
        Args:
            decay_name (str): The name of the decay.
        Returns:
            int: The decay roll value.
        """
        if decay_name not in self.statlets_decay:
            return 0
        value = self.statlets_decay[decay_name]['value']
        static = int(value)
        uni = uniform(0.0, 1.0)
        if uni < value - static:
            static += 1
        return -static if self.statlets_decay[decay_name]['sign'] else static


    def create_statlet(self, *, target: str, value: int, decay: float, decay_sign=True) -> bool:
        """
        Creates a new statlet and adds it to the `statlets` dictionary.
        Args:
            target (str): The name of the statlet to be created.
            value (int): The value of the statlet.
        Returns:
            bool: True if the statlet is created and added successfully, False otherwise.
        """
        if target not in self.mood_stats and target not in self.personality_stats:
            return False

        self.statlets[target] = value
        self.statlets_decay[target] = {'value': decay, 'sign': decay_sign}
        return True
    
if __name__ == '__main__':
    test1 = Entity(Mood=50, Social=50, World=50, Information=50, Decision=50)
    test2 = Entity()

    print(test2.mood_stats)
