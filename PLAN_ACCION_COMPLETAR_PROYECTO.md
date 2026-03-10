# 🎯 PLAN DE ACCIÓN: QUÉ HACER AHORA

**Para completar VIT de 42% a 100% en tiempo**

---

## DIAGNOSTICO RÁPIDO

- ✅ Backend core: 42% completo
- ❌ SGSI core: 0% completo (Risk/SoA/Evidence)
- ❌ Frontend: 5% completo
- ⚠️ Tests: Informal, necesita pytest

---

## OPCIÓN 1: COMPLETAR EN 8 SEMANAS (Full Sprint)

### Semana 1-2: CRITICAL PATH (Risk + SoA)

#### **Día 1-3: Risk Model**
```python
# backend/apps/risks/models.py
class Risk(models.Model):
    project = FK(Project)
    description = CharField()
    
    # Inherent
    inherent_probability = IntegerField(1-5)
    inherent_impact = IntegerField(1-5)
    inherent_score = IntegerField()  # Auto-calc: prob × impact
    
    # Residual (after controls)
    residual_probability = IntegerField(1-5)
    residual_impact = IntegerField(1-5) 
    residual_score = IntegerField()  # Auto-calc
    
    # Treatment
    control_type = CharField(choices=['MITIGATE', 'ACCEPT', 'AVOID'])
    status = CharField(choices=['IDENTIFIED', 'MITIGATED', 'ACCEPTED'])
    
    created_by = FK(User)
    created_at, updated_at = timestamps
```

**Tiempo**: 6 horas (model + serializer + viewset + tests + demo)

#### **Día 4: ISOControl + SoAItem**
```python
# backend/apps/iso_controls/models.py
class ISOControl(models.Model):
    code = CharField(UNIQUE)  # A.5.1, A.5.2, ..., A.9.7
    name = CharField()
    description = TextField()
    category = CharField()
    
    # Auto-generate via loaddata fixture with 93 controls

class SoAItem(models.Model):
    project = FK(Project)
    control = FK(ISOControl)
    is_applicable = BooleanField()
    justification = TextField(blank=True)  # Si NO aplica
    impl_status = CharField(choices=['NOT_IMPL', 'IN_PROGRESS', 'IMPLEMENTED'])
    responsible = FK(User, null=True)
    
    created_at, updated_at
```

**Tiempo**: 8 horas (models + auto-generation signal + serializers + viewsets)

#### **Día 5-6: Evidence**
```python
# backend/apps/evidence/models.py
class Evidence(models.Model):
    soaitem = FK(SoAItem)
    uploaded_by = FK(User)
    
    file = FileField()
    version = IntegerField()
    status = CharField(choices=['PENDING', 'APPROVED', 'REJECTED'])
    
    comments = TextField(blank=True)
    approved_by = FK(User, null=True)
    
    created_at, updated_at
    
    # Signal: when Evidence.status='APPROVED' → update SoAItem.impl_status='IMPLEMENTED'
```

**Tiempo**: 6 horas

#### **Día 7: Tests + Integration**
```
Total Semana 1-2: 20 horas → Risk + SoA + Evidence FUNCIONAL
```

---

### Semana 3: Frontend Login

#### **Day 1: Login Component**
```jsx
// frontend/src/pages/Login.jsx
import { useState } from 'react'
import axios from 'axios'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  
  const handleLogin = async (e) => {
    e.preventDefault()
    const res = await axios.post('http://localhost:8000/api/token/', {
      username, password
    })
    localStorage.setItem('access', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
    navigate('/dashboard')
  }
  
  return (
    <form onSubmit={handleLogin}>
      <input value={username} onChange={e => setUsername(e.target.value)} />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button>Login</button>
    </form>
  )
}
```

**Tiempo**: 3 horas

#### **Day 2: PrivateRoute + Dashboard skeleton**
```jsx
// frontend/src/components/PrivateRoute.jsx
import { Navigate } from 'react-router-dom'

export function PrivateRoute({ children }) {
  const token = localStorage.getItem('access')
  return token ? children : <Navigate to="/login" />
}

// frontend/src/pages/Dashboard.jsx
import { useState, useEffect } from 'react'
import axios from 'axios'

export default function Dashboard() {
  const [user, setUser] = useState(null)
  
  useEffect(() => {
    const token = localStorage.getItem('access')
    axios.get('http://localhost:8000/api/users/me/', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setUser(res.data))
  }, [])
  
  if (!user) return <div>Loading...</div>
  
  return (
    <div>
      <h1>Dashboard - {user.role}</h1>
      {user.role === 'ADMIN' && <AdminDash />}
      {user.role === 'CONSULTANT' && <ConsultantDash />}
      {user.role === 'CLIENT' && <ClientDash />}
    </div>
  )
}
```

**Tiempo**: 4 horas

---

### Semana 4-5: Project management UI

- Project list
- Project detail
- Create project form
- Phase/Task UI

**Time**: 16 horas

---

### Semana 6: Risk + SoA UI

- Risk matrix (5×5 visualization)
- SoA table (93 controls)
- Evidence upload form

**Time**: 12 horas

---

### Semana 7: Reports + Polish

- SoA PDF generation
- Dashboard charts
- Error handling
- Polish UI

**Time**: 12 horas

---

### Semana 8: Testing + Deployment

- Pytest formal test suite
- Docker + docker-compose
- GitHub CI/CD
- Final QA

**Time**: 16 horas

---

**TOTAL: ~80 horas = 2 weeks @ 40 hrs/week = DOABLE**

---

## OPCIÓN 2: MVP (Minimum Viable) - 4 SEMANAS

**Si solo tienes 4 semanas:**

### Semana 1: Risk + SoA models (BACKEND ONLY)
- Risk model + serializer + viewset + tests
- ISOControl (fixture with 93 controls)
- SoAItem auto-generation
- Evidence model + file upload

**Time**: 20 horas

### Semana 2: Frontend login + Dashboard
- Login page
- PrivateRoute
- Dashboard skeleton (3 versions by role)
- Project list

**Time**: 20 horas

### Semana 3: Risk/SoA UI
- Risk matrix
- SoA table
- Evidence grid

**Time**: 12 horas

### Semana 4: Tests + fixes
- Pytest suite
- Bug fixes
- Polish

**Time**: 12 horas

**TOTAL: 64 horas (MVP funcional)**

---

## OPCIÓN 3: EXTEND SPRINT 1 ONLY - 1 WEEK

**Si solo tienes 1 semana más:**

- ✅ Keep existing backend (Auth/RBAC/Projects)
- ✅ Implement Risk model (BARE MINIMUM)
- ✅ Implement SoAItem (BARE MINIMUM)
- ❌ Skip Evidence (for now)
- ❌ Skip Frontend (for now)
- ✅ Write formal tests

**This gets you to 50% completion, but SGSI is incomplete.**

---

## RECOMENDACIÓN PROFESIONAL

### Para un profesor que evalúa:

**Demuestra esto:**

1. **Day 1-2**: Risk model working (POST /api/risks/, inherent/residual score calculated)
2. **Day 3**: ISOControl + SoAItem auto-generation (93 controls precargados)
3. **Day 4**: Evidence model + file upload
4. **Day 5**: Frontend login page wired to /api/token/
5. **Day 6**: Dashboard skeleton (read-only)
6. **Day 7**: Formal pytest test suite (min 20 test cases)

**If you can show this in 1 week**: Score = 7/10 (good effort, incomplete frontend)  
**If you can show this + polish**: Score = 8/10 (minor gaps)

---

## NO HACER (Waste of Time)

❌ Spend time on UI Polish (buttons, colors) → Focus on FEATURES  
❌ Spend time on Docker (if no time left) → You need SGSI features  
❌ Spend time on advanced reports (PDF/Excel) → Basic JSON is enough  
❌ Spend time on notifications → Not critical  

---

## DO SPEND TIME ON

✅ Risk + SoA + Evidence (THE CORE)  
✅ Formal tests (pytest, >50% coverage)  
✅ Frontend login + Dashboard  
✅ AuditLog properly linked to all changes  

---

## COMMIT SEQUENCE (GIT)

```
Day 1: git commit -m "Feature: Risk model with inherent/residual score calculation"
Day 2: git commit -m "Feature: ISOControl (93 controls) + SoAItem auto-generation"
Day 3: git commit -m "Feature: Evidence model with file upload"
Day 4: git commit -m "Feature: Frontend login + PrivateRoute"
Day 5: git commit -m "Feature: Dashboard skeleton with 3 role-based versions"
Day 6: git commit -m "Test: Pytest suite with 25+ test cases"
Day 7: git commit -m "Polish: UI/UX improvements and error handling"

git tag v0.2-sprint2
```

---

## SUCCESS CRITERIA

At the end of 1 week, you should have:

```
✅ Risk model fully functional
✅ SoA with 93 controls precargado
✅ Evidence upload working
✅ Frontend login → Dashboard
✅ Pytest test suite >50 passing tests
✅ 0 errors 500 in production code
✅ All migrations applied cleanly
✅ Clean git history with 7+ descriptive commits
```

**If you achieve this**: You have a FUNCTIONAL SGSI platform (60-70% complete).

---

## WORST-CASE SCENARIO (If you only do 3 days)

1. Implement Risk model
2. Implement SoAItem auto-gen
3. Write tests + demo

**Result**: You prove YOU UNDERSTAND the SGSI architecture, even if incomplete.

---

**Good luck! You have the foundation. Build on it.** 🚀

---

*Plan created: 10 March 2026*  
*Realistic timeline: 4-8 weeks to completion*  
*MVP (minimum viable): 1-2 weeks with focus*
