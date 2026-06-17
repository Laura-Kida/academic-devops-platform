import { useEffect, useState } from "react"
import "./App.css"

const AUTH_API = import.meta.env.VITE_AUTH_API_URL || "http://localhost:8001"
const ACADEMIC_API =
  import.meta.env.VITE_ACADEMIC_API_URL || "http://localhost:8002"

function App() {
  const [email, setEmail] = useState("aluno@escola.br")
  const [senha, setSenha] = useState("senha123")
  const [perfil, setPerfil] = useState("aluno")
  const [token, setToken] = useState(localStorage.getItem("token") || "")
  const [courses, setCourses] = useState([])
  const [newCourse, setNewCourse] = useState("")
  const [message, setMessage] = useState("")

  async function registerUser() {
    setMessage("Criando usuário...")

    try {
      const response = await fetch(`${AUTH_API}/usuarios`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          senha,
          perfil,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        setMessage(data.detail || "Erro ao criar usuário")
        return
      }

      setMessage("Usuário criado com sucesso! Agora faça login.")
    } catch {
      setMessage("Erro de conexão com o Auth Service")
    }
  }

  async function login() {
    setMessage("Fazendo login...")

    try {
      const response = await fetch(`${AUTH_API}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          senha,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        setMessage(data.detail || "Erro ao fazer login")
        return
      }

      localStorage.setItem("token", data.token)
      setToken(data.token)
      setMessage("Login realizado com sucesso!")
    } catch {
      setMessage("Erro de conexão com o Auth Service")
    }
  }

  async function loadCourses() {
    setMessage("Carregando cursos...")

    try {
      const response = await fetch(`${ACADEMIC_API}/courses`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      const data = await response.json()

      if (!response.ok) {
        setMessage(data.detail || "Erro ao buscar cursos")
        return
      }

      setCourses(data)
      setMessage("Cursos carregados com sucesso!")
    } catch {
      setMessage("Erro de conexão com o Academic Service")
    }
  }

  async function createCourse() {
    if (!newCourse.trim()) {
      setMessage("Digite o nome do curso")
      return
    }

    try {
      const response = await fetch(`${ACADEMIC_API}/courses`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: newCourse,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        setMessage(data.detail || "Erro ao criar curso")
        return
      }

      setNewCourse("")
      setMessage(`Curso "${data.name}" criado com sucesso!`)
      loadCourses()
    } catch {
      setMessage("Erro de conexão com o Academic Service")
    }
  }

  function logout() {
    localStorage.removeItem("token")
    setToken("")
    setCourses([])
    setMessage("Logout realizado")
  }

  useEffect(() => {
    if (token) {
      loadCourses()
    }
  }, [token])

  return (
    <main className="page">
      <section className="card">
        <h1>Plataforma Acadêmica DevOps</h1>
        <p className="subtitle">
          Integração entre Frontend, Auth Service e Academic Service
        </p>

        <div className="grid">
          <div className="panel">
            <h2>Login e Cadastro</h2>

            <label>Email</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="aluno@escola.br"
            />

            <label>Senha</label>
            <input
              type="password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              placeholder="senha123"
            />

            <label>Perfil</label>
            <select value={perfil} onChange={(e) => setPerfil(e.target.value)}>
              <option value="aluno">Aluno</option>
              <option value="professor">Professor</option>
            </select>

            <div className="button-group">
              {!token ? (
                <>
                  <button onClick={login}>Entrar</button>
                  <button onClick={registerUser} className="secondary">
                    Criar cadastro
                  </button>
                </>
              ) : (
                <button onClick={logout} className="danger">
                  Sair
                </button>
              )}
            </div>

            {token && (
              <p className="token">
                Token ativo: <strong>{token}</strong>
              </p>
            )}
          </div>

          <div className="panel">
            <h2>Cursos</h2>

            <button onClick={loadCourses} disabled={!token}>
              Atualizar cursos
            </button>

            <div className="create-course">
              <input
                value={newCourse}
                onChange={(e) => setNewCourse(e.target.value)}
                placeholder="Nome do novo curso"
                disabled={!token}
              />
              <button onClick={createCourse} disabled={!token}>
                Criar
              </button>
            </div>

            <ul className="course-list">
              {courses.map((course) => (
                <li key={course.id}>
                  <span>#{course.id}</span> {course.name}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {message && <div className="message">{message}</div>}
      </section>
    </main>
  )
}

export default App