import { useState } from "react";

function Login() {
  // Estados para armazenar os valores das caixas de texto
  const [matricula, setMatricula] = useState("");
  const [senha, setSenha] = useState("");

  // Função chamada quando o botão de login for pressionado
  const handleLogin = () => {
    console.log("Matrícula:", matricula);
    console.log("Senha:", senha);
  };

  return (
    <div style={styles.container}>
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Matrícula"
        value={matricula}
        onChange={(e) => setMatricula(e.target.value)}
        style={styles.input}
      />
      <input
        type="password"
        placeholder="Senha"
        value={senha}
        onChange={(e) => setSenha(e.target.value)}
        style={styles.input}
      />
      <button onClick={handleLogin} style={styles.button}>Entrar</button>
    </div>
  );
}

// Estilos em objeto JavaScript
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    backgroundColor: "#f4f4f4",
  },
  input: {
    width: "200px",
    padding: "10px",
    margin: "5px",
    border: "1px solid #ccc",
    borderRadius: "5px",
  },
  button: {
    width: "220px",
    padding: "10px",
    marginTop: "10px",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
};

export default Login;
