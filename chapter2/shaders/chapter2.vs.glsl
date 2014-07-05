#version 410 core
layout (location = 1) in vec4 m_offset;
layout (location = 2) in vec4 m_vertex;
layout (location = 3) in vec4 m_color;
out vec4 color;

void main()
{
    gl_Position = m_vertex + m_offset;
    color = m_color;
}