import numpy as np

from utils import DNDict, PQ, Vert

class Turtle:
    def __init__(self, maze, start, goal):
        # Actual
        self.start = np.array(start)
        self.goal = np.array(goal)
        self._maze = maze # Unknown maze
        self.actual_pos = self.start.copy()
        self.unit_vecs = np.array(((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)))

        # Algorithm requirements
        self._g = DNDict(lambda k: np.inf)
        self._search = DNDict(lambda k: np.inf)
        self._c = DNDict(lambda k: 1)
        self._h = DNDict(lambda k: self._H(k, self.goal))
        self._closed = set()
        self.counter = 0
        self._nodes = DNDict(lambda k: Vert(k), True)

        # Printing requirements
        self.history = []

    def Move(self, new_pos):
        # print 'moving to:'
        # print new_pos
        if any(new_pos < 0):
            raise EnvironmentError('Attempted move into disallowed square.')
        if self._maze[tuple(new_pos)] == np.inf:
            raise EnvironmentError('Attempted move into disallowed square.')
        if self._H(new_pos, self.actual_pos) != 1:
            raise EnvironmentError('Attempted to move more than one square.')
        self.actual_pos = new_pos.copy()
        self.history.append(new_pos.copy())

    def Observe(self):
        # print 'observing'
        # scan actual maze:
        pos_with_decreased_cost = []
        did_observe_change = False
        for unit_vec in self.unit_vecs:
            pos_to_scan = unit_vec + self.actual_pos
            if any(pos_to_scan < 0):
                actual_cost = np.inf
            else:
                try:
                    actual_cost = self._maze[tuple(pos_to_scan)]
                except IndexError:
                    actual_cost = np.inf
            if actual_cost > self._c[pos_to_scan]:
                self._nodes[pos_to_scan].next = None
                self._c[pos_to_scan] = actual_cost
                did_observe_change = True
            elif actual_cost < self._c[pos_to_scan]:
                self._c[pos_to_scan] = actual_cost
                pos_with_decreased_cost.append([self.start, pos_to_scan])
                did_observe_change = True

        if len(pos_with_decreased_cost) > 0:
            self.Reestablish_consistency(pos_with_decreased_cost)
        return did_observe_change

    def _H(self, A, B):
        return np.sum(np.abs(A-B))

    def Initialize_state(self, s_v):
        # print 'Initialize_state'
        if self._search[s_v.pos] != self.counter:
            # self._g[s_v] = np.inf
            # # Equivalent to:
            del self._g[s_v.pos]
        self._search[s_v.pos] = self.counter

    def Build_path(self, s_v):
        # print 'building path'
        while any(s_v.pos != self.start):
            s_v.parent.next = s_v
            s_v = s_v.parent
        return s_v

    def A_star(self, s_init_v):
        # print 'A*'
        g, c, h = self._g, self._c, self._h
        self.Initialize_state(s_init_v)
        s_init_v.parent = None
        self._g[s_init_v.pos] = 0
        Open = PQ()
        Open.push(s_init_v, g[s_init_v.pos] + h[s_init_v.pos])
        self._closed = set()
        while True:
            try:
                s_v = Open.pop()
            except KeyError:
                break
            if self.A_star_goal_condition(s_v):
                return s_v
            else:
                self._closed.add(s_v)
            for s_prime_v in self.Succ(s_v):
                self.Initialize_state(s_prime_v)
                if g[s_prime_v.pos] > g[s_v.pos] + c[s_prime_v.pos]:
                    g[s_prime_v.pos] = g[s_v.pos] + c[s_prime_v.pos]
                    s_prime_v.parent = s_v
                    # Overwrites current priority:
                    Open.push(s_prime_v, g[s_prime_v.pos] + h[s_prime_v.pos])
        return None

    def Succ(self, s_v):
        # print 'succession'
        if self._c[s_v.pos] == np.inf:
            return
        else:
            for unit_vec in self.unit_vecs:
                node_to_yield = self._nodes[s_v.pos + unit_vec]
                if self._c[node_to_yield.pos] != np.inf:
                    yield node_to_yield


    def Main(self):
        self.Observe()

        while any(self.start != self.goal):
            self.counter += 1
            s = self.A_star(self._nodes[self.start])
            if s is None:
                raise EnvironmentError('Goal is not reachable.')

            for s_prime in self._closed:
                self._h[s_prime.pos] = self._g[s.pos] + self._h[s.pos] - self._g[s_prime.pos]

            start_vert = self.Build_path(s)

            did_observe_change = False

            while any(self.start != self.goal) and not did_observe_change:
                t = start_vert
                if start_vert.next is not None:
                    start_vert = start_vert.next
                    t.next = None
                    self.start = start_vert.pos

                    self.Move(self.start)
                    did_observe_change = self.Observe()
                else:
                    pass
        return 'Found goal!'

    def A_star_goal_condition(self, s_vert):
        # print 'goal condition'
        while (s_vert.next is not None
                and self._h[s_vert.pos] == self._h[s_vert.next.pos]
                    + self._c[s_vert.next.pos]):
            s_vert = s_vert.next
        return all(s_vert.pos == self.goal)

    def Insert_state(self, s, s_prime, Q):
        # print 'inserting state'
        s_v = self._nodes[s]
        s_prime_v = self._nodes[s_prime]
        if self._h[s_v.pos] > self._c[s_prime_v.pos] + self._h[s_prime_v.pos]:
            self._h[s_v.pos] = self._c[s_prime_v.pos] + self._h[s_prime_v.pos]
            s_v.next = None
            s_v.support = s_prime_v

            Q.push(s_v, self._h[s_v.pos])

    def Reestablish_consistency(self, edges_with_lowered_cost):
        # print 'reestconst'
        Q = PQ()
        for s, s_prime in edges_with_lowered_cost:
            self.Insert_state(s, s_prime, Q)

        for s_prime_v in Q:
            if s_prime_v.support.next is not None:
                s_prime_v.next = s_prime_v.support

            # This assumes bidirectionality, should be
            # ```for each s such that s_prime is in Succ(s) do```
            for s_v in self.Succ(s_prime_v):
                self.Insert_state(s_v, s_prime_v, Q)
