import pygame
import copy
import numpy

storePointCoordinates = []
storeConnectionsAtPoints = []
globalKirchoffVoltage = []
storeConnectionReference = []


class component:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class wire(component):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.current = 0

class voltage_source(component):
    def __init__(self, x1, y1, x2, y2, voltage=5):
        super().__init__(x1, y1, x2, y2)
        self.voltage = voltage
        self.current = 0

class resistor(component):
    def __init__(self, x1, y1, x2, y2, resistance=1000):
        super().__init__(x1, y1, x2, y2)
        self.resistance = resistance
        self.voltage = 0
        self.current = 0

class capacitor(component):
    def __init__(self, x1, y1, x2, y2, capacitance=0.001):
        super().__init__(x1, y1, x2, y2)
        self.capacitance = capacitance
        self.voltage = 0
        self.current = 0

class inductor(component):
    def __init__(self, x1, y1, x2, y2, inductance=0.000001):
        super().__init__(x1, y1, x2, y2)
        self.inductance = inductance
        self.voltage = 0
        self.current = 0


components = []

def place_component(component_type, x1, y1, x2, y2):
    print()
    print("--------PLACE COMPONENT START--------")
    # will not allow component with same start and end point
    if x1 == x2 and y1 == y2:
        return
    
    if component_type == "wire":
        new_component = wire(x1, y1, x2, y2)
    elif component_type == "voltage_source":
        new_component = voltage_source(x1, y1, x2, y2)
    elif component_type == "resistor":
        new_component = resistor(x1, y1, x2, y2)
    elif component_type == "capacitor":
        new_component = capacitor(x1, y1, x2, y2)
    elif component_type == "inductor":
        new_component = inductor(x1, y1, x2, y2)

    else:
        raise ValueError("Unknown component type")
    
    a = 0
    b = 0
    
    # Check if the points already exist in storePointCoordinates
    if storePointCoordinates != 0:
        for i, point in enumerate(storePointCoordinates):
            if point[0] == x1 and point[1] == y1:
                storeConnectionsAtPoints[i].append((len(components), 0))
                a = 1
            if point[0] == x2 and point[1] == y2:
                storeConnectionsAtPoints[i].append((len(components), 1))
                b = 1
    if a == 0:
        storePointCoordinates.append((x1, y1))
        storeConnectionsAtPoints.append([(len(components), 0)])
    if b == 0:
        storePointCoordinates.append((x2, y2))
        storeConnectionsAtPoints.append([(len(components), 1)])
    
    print()
    print("storePointCoordinates:", storePointCoordinates)
    print("storeConnectionsAtPoints", storeConnectionsAtPoints)
    components.append(new_component)

    del storeConnectionReference[:]
    for i, nodeA in enumerate(storeConnectionsAtPoints):
        referenceAtNode = []
        for w, componentA in enumerate(nodeA):
            for k, nodeB in enumerate(storeConnectionsAtPoints):
                if k != i:
                    for x, componentB in enumerate(nodeB):
                        if componentA[0] == componentB[0]:
                            referenceAtNode.append(k)
        storeConnectionReference.append(referenceAtNode)
    
    print("storeConnectionReference", storeConnectionReference)

    global globalKirchoffVoltage
    globalKirchoffVoltage = manage_voltage_law()
    print("Voltage laws:", globalKirchoffVoltage)
    
#    KirchoffCurrent, JunctionConnections = manage_current_law()
#    if KirchoffCurrent == None:
#        KirchoffCurrent = KirchoffVoltage
#    print("Current laws:", KirchoffCurrent)
#    print("JunctionConnections:", JunctionConnections)

    if (globalKirchoffVoltage is not None):
        solution = solve(globalKirchoffVoltage)

def manage_voltage_law():
    nodesExplored = []
    componentConnections = []
    print("storeConnectionsAtPoints", storeConnectionsAtPoints)
    #Find the point for which the loope will be created
    a = False
    for i, point in enumerate(storeConnectionsAtPoints):
        if len(storeConnectionsAtPoints[i]) > 2:
            a = True
            if storeConnectionsAtPoints[i][0][1] == 0:
                componentConnections.append((storeConnectionsAtPoints[i][0][0], 1))
            else:
                componentConnections.append((storeConnectionsAtPoints[i][0][0], 0))
            for k, nothing in enumerate(storeConnectionsAtPoints):
                if k != i:
                    for w, nothing2 in enumerate(storeConnectionsAtPoints[k]):
                        if storeConnectionsAtPoints[k][w][0] == storeConnectionsAtPoints[i][0][0]:
                            nodesExplored.append(k)
                            nodesExplored.append(i)
            break
        else:
            if len(storeConnectionsAtPoints[i]) > 1:
                a = True
                if storeConnectionsAtPoints[i][0][1] == 0:
                    componentConnections.append((storeConnectionsAtPoints[i][0][0], 1))
                else:
                    componentConnections.append((storeConnectionsAtPoints[i][0][0], 0))
                for k, nothing in enumerate(storeConnectionsAtPoints):
                    if k != i:
                        for w, nothing2 in enumerate(storeConnectionsAtPoints[k]):
                            if storeConnectionsAtPoints[k][w][0] == storeConnectionsAtPoints[i][0][0]:
                                nodesExplored.append(k)
                                nodesExplored.append(i)
                break
            if i == len(storePointCoordinates) - 1:
                return

    if a == False:
        for i, point in enumerate(storeConnectionsAtPoints):
            if len(storeConnectionsAtPoints[i]) > 2:
                a = True
                if storeConnectionsAtPoints[i][0][1] == 0:
                    componentConnections.append((storeConnectionsAtPoints[i][0][0], 1))
                else:
                    componentConnections.append((storeConnectionsAtPoints[i][0][0], 0))
                for k, nothing in enumerate(storeConnectionsAtPoints):
                    if k != i: 
                        for w, nothing2 in enumerate(storeConnectionsAtPoints[k]):
                            if storeConnectionsAtPoints[k][w][0] == storeConnectionsAtPoints[i][0][0]:
                                nodesExplored.append(k)
                                nodesExplored.append(i)
                break
            if i == len(storePointCoordinates) - 1:
                return
    
    
    print("Nodes Explored", nodesExplored)
    print("componentConnections", componentConnections)
    
    hold = create_loops(nodesExplored, componentConnections[0][0], componentConnections[0][1], componentConnections)
    if hold is not None:
        currentLoops = hold
        print("CurrentLoops:", currentLoops)
    return currentLoops

#This is the function that creates the list of the kirchoff loops
def create_loops(nodesExploredInternal, firstComponent, orientation, componentConnections):
    currentLoops = []

    currentNode = nodesExploredInternal[len(nodesExploredInternal) - 1]
    print()
    print("currentNode:", currentNode, "storeConnectionsAtPoints[currentNode]", storeConnectionsAtPoints[currentNode])
    print("nodesExplored:", nodesExploredInternal, "currentloops:", currentLoops)
    #recursive exploration function
    for i, point in enumerate(storeConnectionsAtPoints[currentNode]):
        if point[0] == firstComponent:
            print("point:", point, " first Component")
            continue
        for j, nodeSearched in enumerate(storeConnectionsAtPoints):
            for k, componentSearched in enumerate(nodeSearched):
                if componentSearched[0] == point[0] and componentSearched[1] != point[1]:
                    if j not in nodesExploredInternal:
                        copy1 = copy.copy(nodesExploredInternal)
                        copy2 = copy.deepcopy(componentConnections)
                        print("point:", point, " Unexplored node")
                        copy1.append(j)
                        copy2.append(point)
                        print("CHECK nodesExplored:", nodesExploredInternal)
                        print("CHECK componentConnection", componentConnections)
                        hold = create_loops(copy1, componentSearched[0], orientation, copy2)
                        print("exiting point:", point,"storeConnectionsAtPoints[currentNode]", storeConnectionsAtPoints[currentNode], " hold:", hold)
                        print("CHECK nodesExplored:", nodesExploredInternal)
                        if hold is not None:
                            print("there are no loops")
                            currentLoops += hold
                    elif j == nodesExploredInternal[0]:
                        temp = componentConnections.copy()
                        temp.append(point)
                        print("point:", point, " loop found")
                        print("componentConnections(temp):", temp)
                        print("componentConnections(og):", componentConnections)
                        currentLoops.append(temp)
                        print("currentLoops updated:", currentLoops)
                    else:
                        print("point:", point, " already explored node")
                        continue
    print ("exiting currentNode:", currentNode, " currentLoops:", currentLoops)
    print("CHECK nodesExplored:", nodesExploredInternal)
    return currentLoops
                         


#def manage_current_law():
#    CurrentLists = []
#    MainNodes = []
#    MainNodeConnections = []
#    JunctionConnections = []

#    if len(storeConnectionsAtPoints) < 3:
#        return None, None

#    for point, pointConnections in enumerate(storeConnectionReference):
#        if len(pointConnections) > 2:
#            MainNodes.append(point)
#            MainNodeConnections.append(pointConnections)

 #   if not MainNodes:
 #       for p, point in enumerate(storeConnectionReference):
 #           if len(point) == 1:
 #               print("point : ", point)
 #               CurrentLists.append(iPathfind(p, 0))
 #               return CurrentLists, None
 #       return None, None
 #   else:
 #       for m, main in enumerate(MainNodeConnections):
 #           JunctionHold = []
 #           for i in range(len(main)):
 #               CurrentPath = iPathfind(MainNodes[m], i)
 #               print("Current Path", CurrentPath)
 #               p = False
 #               for v, w in enumerate(CurrentLists):
 #                   print("w[0]", w[0], "CurrentPath[len(CurrentPath) - 1]", CurrentPath[len(CurrentPath) - 1])

#                    if CurrentPath[len(CurrentPath) - 1][0] == w[0][0]:
#                        p = True
#                        JunctionHold.append((v, 1))
#                if p == False:
#                    CurrentLists.append(CurrentPath)
#                    JunctionHold.append(((len(CurrentLists) - 1), 0))
#            JunctionConnections.append(JunctionHold)


#    return CurrentLists, JunctionConnections 





#def iPathfind(startPoint, direction):
#    iPath = []
#    p = False
#    while p == False:
#        if len(storeConnectionReference[storeConnectionReference[startPoint][direction]]) > 2:
#            p = True
#            iPath.append(storeConnectionsAtPoints[startPoint][direction])
#        elif len(storeConnectionReference[storeConnectionReference[startPoint][direction]]) == 1:
#            p = True
#            iPath.append(storeConnectionsAtPoints[startPoint][direction])
#        else:
#            iPath.append(storeConnectionsAtPoints[startPoint][direction])
#            if storeConnectionReference[storeConnectionReference[startPoint][direction]][0] == startPoint:
#                startPoint = storeConnectionReference[startPoint][direction]
#                direction = 1
#            else:
#                startPoint = storeConnectionReference[startPoint][direction]
#                direction = 0
#    return iPath

def extSolve():
    print("globalKirchoffVoltage", globalKirchoffVoltage)
    solve(globalKirchoffVoltage)

def solve(KirchoffVoltage):
    #Ax = B
    MatrixLength = 2 * len(components)
    A = []
    B = []

    store = []
    for w, x in enumerate(KirchoffVoltage):
        add = False
        if w == 0:
            add = True
            for i in x:
                store.append(i[0])
        else:
            for i in x:
                if i[0] not in hold:
                    add = True
                    store.append(i[0])
        if add == True:
            hold = [0] * MatrixLength
            for i in x:
                if i[1] == 0:
                    hold[2 * i[0]] = 1
                else:
                    hold[2 * i[0]] = -1
            A.append(hold)
            B.append(0)

    print("storeConnectionsAtPoint:", storeConnectionsAtPoints)
    for a, x in enumerate(storeConnectionsAtPoints):
        if a + 1 != len(storeConnectionsAtPoints):
            hold = [0] * MatrixLength
            for y in x:
                if y[1] == 0:
                    hold[2 * y[0] + 1] = 1
                if y[1] == 1:
                    hold[2 * y[0] + 1] = -1
            print("hold:", hold)
            A.append(hold)
            B.append(0)


#    for x in KirchoffCurrent:
#        for y in range(len(x) - 1):
#            hold = [0] * MatrixLength
#            hold[2 * x[y][0] + 1] = 1
#            if x[y][1] == x[y + 1][1]:
#                hold[2 * x[y + 1][0] + 1] = -1
#            else:
#                hold[2 * x[y + 1][0] + 1] = 1
#            A.append(hold)
#            B.append(0)


#    for x in range(len(JunctionConnections) - 1):
#        hold = [0] * MatrixLength
#        for y in JunctionConnections[x]:
#            if KirchoffCurrent[y[0]][0][1] == 0:
#                hold[2 * KirchoffCurrent[y[0]][0][0] + 1] = 1
#            else:
#                hold[2 * KirchoffCurrent[y[0]][0][0] + 1] = -1
#        A.append(hold)
#        B.append(0)



    for c, comp in enumerate(components):
        hold = [0] * MatrixLength
        if isinstance(comp, wire):
            hold[2 * c] = 1
            A.append(hold)
            B.append(0)
        elif isinstance(comp, voltage_source):
            hold[2 * c] = 1
            A.append(hold)
            B.append(comp.voltage)
        elif isinstance(comp, resistor):
            hold[2 * c] = 1
            hold[2 * c + 1] = -comp.resistance
            A.append(hold)
            B.append(0)
        elif isinstance(comp, capacitor):
            hold[2 * c] = -comp.capacitance
            hold[2 * c + 1] = 1
            A.append(hold)
            B.append(-comp.capacitance * comp.voltage)
        elif isinstance(comp, inductor):
            hold[2 * c] = 1
            hold[2 * c + 1] = -comp.inductance
            A.append(hold)
            B.append(-comp.inductance * comp.current)

    print("A:", A)
    print("B:", B)
    print("len(A[0])", len(A[0]))
    print("len(A)", len(A))
    a = numpy.array(A)
    b = numpy.array(B)
    if(len(B) > 5):
        cmat = numpy.linalg.solve(a, b)
        print("a", a)
        print("b", b)
        print("c", cmat)

    for c, comp in enumerate(components):
        if isinstance(comp, capacitor):
            comp.voltage = cmat[2*c]

    for c, comp in enumerate(components):
        if isinstance(comp, inductor):
            comp.inductance = cmat[2*c]

    return 0


def display_components(screen, width, height, gridToScreenX, gridToScreenY):
    font = pygame.font.SysFont(None, 18)

    for comp in components:
        x1 = gridToScreenX(comp.x1)
        y1 = gridToScreenY(comp.y1)
        x2 = gridToScreenX(comp.x2)
        y2 = gridToScreenY(comp.y2)

        dx = x2 - x1
        dy = y2 - y1

        # -------------------------------------------------
        # WIRE
        # -------------------------------------------------
        if isinstance(comp, wire):
            pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)

        # -------------------------------------------------
        # VOLTAGE SOURCE (big circle with + and -)
        # -------------------------------------------------
        elif isinstance(comp, voltage_source):
            mx = (x1 + x2) // 2
            my = (y1 + y2) // 2
            r = 18

            # wires to circle
            if abs(dx) > abs(dy):  # horizontal
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (mx - r, my), 2)
                pygame.draw.line(screen, (0, 0, 0), (mx + r, my), (x2, y2), 2)

                plus_pos = (mx - 7, my)
                minus_pos = (mx + 7, my)
            else:  # vertical
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (mx, my - r), 2)
                pygame.draw.line(screen, (0, 0, 0), (mx, my + r), (x2, y2), 2)

                plus_pos = (mx, my - 7)
                minus_pos = (mx, my + 7)

            pygame.draw.circle(screen, (0, 0, 0), (mx, my), r, 2)

            plus = font.render("+", True, (0, 0, 0))
            minus = font.render("-", True, (0, 0, 0))

            screen.blit(plus, plus.get_rect(center=plus_pos))
            screen.blit(minus, minus.get_rect(center=minus_pos))

        # -------------------------------------------------
        # RESISTOR (rectangle)
        # -------------------------------------------------
        elif isinstance(comp, resistor):
            mx = (x1 + x2) // 2
            my = (y1 + y2) // 2
            size = 12

            if abs(dx) > abs(dy):  # horizontal
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (mx - size, my), 2)
                pygame.draw.line(screen, (0, 0, 0), (mx + size, my), (x2, y2), 2)
                pygame.draw.rect(screen, (0, 0, 0), (mx - size, my - 6, size * 2, 12), 2)
            else:  # vertical
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (mx, my - size), 2)
                pygame.draw.line(screen, (0, 0, 0), (mx, my + size), (x2, y2), 2)
                pygame.draw.rect(screen, (0, 0, 0), (mx - 6, my - size, 12, size * 2), 2)

        # -------------------------------------------------
        # CAPACITOR (two plates with visible gap)
        # -------------------------------------------------
        elif isinstance(comp, capacitor):
            mx = (x1 + x2) // 2
            my = (y1 + y2) // 2
            gap = 10  # <- bigger gap now
            plate = 18

            if abs(dx) > abs(dy):  # horizontal
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (mx - gap, my), 2)
                pygame.draw.line(screen, (0, 0, 0), (mx + gap, my), (x2, y2), 2)

                pygame.draw.line(screen, (0, 0, 0), (mx - gap, my - plate // 2), (mx - gap, my + plate // 2), 3)
                pygame.draw.line(screen, (0, 0, 0), (mx + gap, my - plate // 2), (mx + gap, my + plate // 2), 3)

            else:  # vertical
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (mx, my - gap), 2)
                pygame.draw.line(screen, (0, 0, 0), (mx, my + gap), (x2, y2), 2)

                pygame.draw.line(screen, (0, 0, 0), (mx - plate // 2, my - gap), (mx + plate // 2, my - gap), 3)
                pygame.draw.line(screen, (0, 0, 0), (mx - plate // 2, my + gap), (mx + plate // 2, my + gap), 3)

        # -------------------------------------------------
        # INDUCTOR (loops)
        # -------------------------------------------------
        elif isinstance(comp, inductor):
            mx = (x1 + x2) // 2
            my = (y1 + y2) // 2
            loops = 4
            radius = 5

            if abs(dx) > abs(dy):  # horizontal
                total = loops * radius * 2
                start = mx - total // 2

                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (start, my), 2)
                pygame.draw.line(screen, (0, 0, 0), (start + total, my), (x2, y2), 2)

                for i in range(loops):
                    center = start + radius + i * radius * 2
                    pygame.draw.circle(screen, (0, 0, 0), (center, my), radius, 2)

            else:  # vertical
                total = loops * radius * 2
                start = my - total // 2

                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (mx, start), 2)
                pygame.draw.line(screen, (0, 0, 0), (mx, start + total), (x2, y2), 2)

                for i in range(loops):
                    center = start + radius + i * radius * 2
                    pygame.draw.circle(screen, (0, 0, 0), (mx, center), radius, 2)


#    for comp in components:
#        if isinstance(comp, wire):
#            pygame.draw.line(screen, (0, 0, 0), (gridToScreenX(comp.x1), gridToScreenY(comp.y1)), (gridToScreenX(comp.x2), gridToScreenY(comp.y2)), 2)
#        elif isinstance(comp, voltage_source):
#            pygame.draw.line(screen, (0, 255, 0), (gridToScreenX(comp.x1), gridToScreenY(comp.y1)), (gridToScreenX(comp.x2), gridToScreenY(comp.y2)), 2)
#            pygame.draw.circle(screen, (0, 255, 0), (gridToScreenX((comp.x1 + comp.x2) / 2), gridToScreenY((comp.y1 + comp.y2) / 2)), 5)
#        elif isinstance(comp, resistor):
#            pygame.draw.line(screen, (255, 0, 0), (gridToScreenX(comp.x1), gridToScreenY(comp.y1)), (gridToScreenX(comp.x2), gridToScreenY(comp.y2)), 2)
#            pygame.draw.rect(screen, (255, 0, 0), (gridToScreenX((comp.x1 + comp.x2) / 2) - 5, gridToScreenY((comp.y1 + comp.y2) / 2) - 5, 10, 10))
#        elif isinstance(comp, capacitor):
#            pygame.draw.line(screen, (255, 255, 0), (gridToScreenX(comp.x1), gridToScreenY(comp.y1)), (gridToScreenX(comp.x2), gridToScreenY(comp.y2)), 2)
#            pygame.draw.rect(screen, (255, 255, 0), (gridToScreenX((comp.x1 + comp.x2) / 2) - 5, gridToScreenY((comp.y1 + comp.y2) / 2) - 5, 10, 10))
        
