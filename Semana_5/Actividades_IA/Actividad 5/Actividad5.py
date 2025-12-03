from collections import defaultdict, deque

class CoursePlanner:
    def __init__(self):
        # graph['prereq'] = ['course1', 'course2']
        self.graph = defaultdict(list)
        # in_degree['course'] = N (número de prerequisitos)
        self.in_degree = defaultdict(int)
        self.all_courses = set()

    def add_course(self, course: str, prerequisites: list[str] = None):
        """
        Añade una materia y sus pre-requisitos al sistema.
        El grafo se modela como: prereq -> course
        """
        if prerequisites is None:
            prerequisites = []

        # Asegura que todas las materias, incluso las sin pre-requisitos,
        # estén en el set y tengan una entrada de in_degree (con 0).
        self.all_courses.add(course)
        if course not in self.in_degree:
            self.in_degree[course] = 0

        for prereq in prerequisites:
            # Añadir la arista del grafo: prereq -> course
            self.graph[prereq].append(course)
            # Incrementar el contador de pre-requisitos para 'course'
            self.in_degree[course] += 1
            # Asegurar que el pre-requisito también exista en el sistema
            if prereq not in self.all_courses:
                 self.all_courses.add(prereq)
                 if prereq not in self.in_degree:
                    self.in_degree[prereq] = 0

    def generate_study_plan(self):
        """
        Genera un plan de estudios óptimo usando el algoritmo de Kahn (Topological Sort).
        
        Responde a las tareas 2, 3, 4 y 5.
        """
        
        # 1. Inicializar la cola (queue) con materias sin pre-requisitos (in-degree == 0)
        # Estas son las materias del primer "semestre"
        queue = deque()
        for course in self.all_courses:
            if self.in_degree[course] == 0:
                queue.append(course)
        
        semesters = [] # Aquí guardaremos el plan (Tarea 3)
        total_courses_sorted = 0 # Contador para detectar ciclos (Tarea 2)

        while queue:
            # Las materias en la cola en este momento se pueden tomar en paralelo (Tarea 4)
            current_semester_courses = []
            
            # Procesar todas las materias del semestre actual
            for _ in range(len(queue)):
                course = queue.popleft()
                current_semester_courses.append(course)
                total_courses_sorted += 1
                
                # "Completar" esta materia. Reducir el in-degree de sus dependientes.
                for dependent_course in self.graph[course]:
                    self.in_degree[dependent_course] -= 1
                    
                    # Si un curso dependiente ya no tiene más pre-requisitos,
                    # añadirlo a la cola para el *próximo* semestre.
                    if self.in_degree[dependent_course] == 0:
                        queue.append(dependent_course)
            
            semesters.append(current_semester_courses)
        
        # Tarea 2: Detección de Ciclos
        if total_courses_sorted != len(self.all_courses):
            # No se pudieron ordenar todas las materias, ¡hay un ciclo!
            # Identificar las materias en el ciclo (son las que tienen in_degree > 0)
            courses_in_cycle = [c for c in self.all_courses if self.in_degree[c] > 0]
            return {
                "success": False,
                "error": "Configuración inválida: Se detectó una dependencia circular.",
                "courses_in_cycle": courses_in_cycle
            }

        # Tareas 3, 4 y 5:
        return {
            "success": True,
            "min_semesters": len(semesters), # Tarea 5
            "study_plan": semesters # Tareas 3 y 4
        }
    

planner = CoursePlanner()

# Añadiendo 10 materias
planner.add_course("CS101: Intro Programación")
planner.add_course("MATH101: Discretas")
planner.add_course("CS102: Estructuras de Datos", prerequisites=["CS101", "MATH101"])
planner.add_course("CS201: Algoritmos", prerequisites=["CS102"])
planner.add_course("CS210: Arquitectura", prerequisites=["CS101"])
planner.add_course("CS301: Sist. Operativos", prerequisites=["CS102", "CS210"])
planner.add_course("CS320: Bases de Datos", prerequisites=["CS102"])
planner.add_course("CS350: Lenguajes de Prog.", prerequisites=["CS102"])
planner.add_course("CS400: IA", prerequisites=["CS201"])
planner.add_course("CS410: Compiladores", prerequisites=["CS201", "CS210"])

# Generar el plan
plan = planner.generate_study_plan()
print('Plan valido')

if plan["success"]:
    print(f"✅ Plan de estudios generado exitosamente.")
    print(f"🎓 Semestre mínimo para graduarse: {plan['min_semesters']}\n")
    
    for i, semester_courses in enumerate(plan['study_plan']):
        print(f"--- Semestre {i+1} ---")
        print(f"(Se pueden tomar en paralelo: {len(semester_courses)} materias)")
        for course in semester_courses:
            print(f"  - {course}")
else:
    print(f"❌ Error: {plan['error']}")
    print(f"Materias involucradas en el ciclo: {plan['courses_in_cycle']}")



#Plan invalido 
print('Plan invalido')
cyclic_planner = CoursePlanner()
cyclic_planner.add_course("Materia A", prerequisites=["Materia C"])
cyclic_planner.add_course("Materia B", prerequisites=["Materia A"])
cyclic_planner.add_course("Materia C", prerequisites=["Materia B"]) # ¡Ciclo!

plan = cyclic_planner.generate_study_plan()

if not plan["success"]:
    print(f"❌ Error: {plan['error']}")
    print(f"Materias involucradas en el ciclo: {plan['courses_in_cycle']}")