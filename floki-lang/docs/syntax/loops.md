# Floki: Loops and Control Flow

This document is part of the **Floki Syntax Module** and describes various mechanisms for controlling execution flow and organizing loops, optimized for event-driven robotics. It belongs in the `/docs/syntax/` directory alongside other syntax-related files.

---

## **1. Understanding Event-Driven Execution in Floki**
Floki follows an **event-driven model**, meaning execution is **reactive**, based on sensor inputs and triggers. Unlike traditional imperative loops (like `while` in C), Floki loops integrate deeply with event handling, ensuring efficient control without blocking execution.

---

## **2. Loop Constructs**

### **2.1 `loop` (Analog of `while`)**
A `loop` runs while a given condition is true.

#### **Syntax:**
```floki
loop imu_pitch > 20 {
    event "adjust_balance"
}
```

#### **Bytecode (FUF):**
```
LABEL_LOOP:
CMP SENSOR[imu_pitch] > 20
JUMP_IF_FALSE LABEL_END
EXEC_EVENT "adjust_balance"
JUMP LABEL_LOOP
LABEL_END:
```

---

### **2.2 `for` (Counting Loop, like C's `for`)**
A `for` loop runs a set number of times.

#### **Syntax:**
```floki
for i = 0 to 10 {
    event "move_forward"
}
```

#### **Bytecode (FUF):**
```
MOV i, 0
LABEL_LOOP:
CMP i, 10
JUMP_IF_GREATER LABEL_END
EXEC_EVENT "move_forward"
ADD i, 1
JUMP LABEL_LOOP
LABEL_END:
```

---

### **2.3 `for each` (Loop Through a List)**
Iterates through a collection.

#### **Syntax:**
```floki
for each paw in paws {
    event "lift_paw" (paw)
}
```

#### **Bytecode (FUF):**
```
ITER_START paws
LABEL_LOOP:
ITER_NEXT paw
JUMP_IF_NULL LABEL_END
EXEC_EVENT "lift_paw" (paw)
JUMP LABEL_LOOP
LABEL_END:
```

---

### **2.4 `every ... do` (Periodic Loop with Timer)**
Executes an event every specified interval. **This loop does not block other executions** and runs asynchronously using an internal timer.

#### **Syntax:**
```floki
every 100ms do {
    read_sensor "imu_pitch"
    if imu_pitch > 20 {
        event "adjust_balance"
    }
}
```

#### **Bytecode (FUF):**
```
TIMER_SET 100ms, LABEL_LOOP
LABEL_LOOP:
EXEC_EVENT "adjust_balance"
TIMER_WAIT
JUMP LABEL_LOOP
```

---

### **2.5 `do ... while` (Execute at Least Once)**
Runs at least once before checking the condition.

#### **Syntax:**
```floki
do {
    event "scan_environment"
} while obstacle_detected
```

#### **Bytecode (FUF):**
```
LABEL_LOOP:
EXEC_EVENT "scan_environment"
CMP SENSOR[obstacle_detected] > 0
JUMP_IF_TRUE LABEL_LOOP
```

---

## **3. Advanced Flow Control**

### **3.1 `match` (Switch-Case Equivalent)**
Checks multiple conditions efficiently using a jump table.

#### **Syntax:**
```floki
match imu_pitch {
    > 20 -> event "stand_up"
    10..20 -> event "adjust_balance"
    < -20 -> event "fall_detected"
    else -> event "minor_adjustment"
}
```

---

### **3.2 `event ... when` (Conditional Event Triggering)**
Triggers an event when a condition is met. **Can be `once` or `repeat`.**

#### **Syntax:**
```floki
event "stand_up" when imu_pitch > 20 repeat
event "alarm" when temperature > 100 once
```

#### **Bytecode (FUF):**
```
EVENT_TRIGGER_REPEAT SENSOR[imu_pitch] > 20 -> EXEC_EVENT "stand_up"
EVENT_TRIGGER_ONCE SENSOR[temperature] > 100 -> EXEC_EVENT "alarm"
```

---

## **4. Control Flow Operators**

### **4.1 `break` (Exit a Loop Early)**
```floki
loop imu_pitch > 20 {
    if foot_pressure < 0.2 {
        break
    }
    event "adjust_balance"
}
```

---

### **4.2 `continue` (Skip an Iteration)**
```floki
for i = 0 to 10 {
    if i == 5 {
        continue
    }
    event "move_forward"
}
```

---

## **5. Error Handling in Loops**
If an event fails during execution, Floki allows handling exceptions using `try-catch`.

```floki
event "sensor_check" when imu_pitch > 20 {
    try {
        read_sensor "imu_pitch"
    } catch {
        log "Sensor failure"
    }
}
```

---

## **6. FUF Instruction Set Overview**

```
CMP A, B         # Compare A with B
JUMP LABEL       # Unconditional jump
JUMP_IF_FALSE L  # Jump if condition is false
EXEC_EVENT "X"   # Execute event
WAIT 100ms       # Wait for a duration
```

---

## **7. Next Steps**
1. **Confirm final syntax.**
2. **Integrate these loops into the Floki compiler (`floki_to_fuf.py`).**
3. **Add automated tests for each loop type.**
4. **Expand documentation with real-world robotic examples.**
5. **Clarify event interactions for `every ... do` and `event ... when`.**
6. **Expand FUF instruction set documentation.**

🚀 **This document ensures Floki's loop and control flow system is clear, structured, and optimized for robotic applications.**

