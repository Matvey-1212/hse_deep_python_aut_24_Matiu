#include <Python.h>
#include <stdio.h>
#include <string.h>

static const char *skip_whitespace(const char *json_str) {
  while (*json_str == ' ' || *json_str == '\t' || *json_str == '\n' ||
         *json_str == '\r') {
    json_str++;
  }
  return json_str;
}

static PyObject *parse_json_string(const char **json_str) {
  (*json_str)++;
  const char *value_start = *json_str;
  while (**json_str != '"') {
    if (**json_str == '\0') {
      PyErr_Format(PyExc_TypeError, "Expected string");
      return NULL;
    }
    (*json_str)++;
  }
  size_t value_len = *json_str - value_start;
  char *value_str = malloc(value_len + 1);
  if (!value_str) {
    return NULL;
  }
  strncpy(value_str, value_start, value_len);
  value_str[value_len] = '\0';
  (*json_str)++;
  PyObject *result = Py_BuildValue("s", value_str);
  free(value_str);
  return result;
}

static PyObject *parse_json_numeric(const char **json_str) {
  char *endptr;
  double num_value = strtod(*json_str, &endptr);
  if (endptr == *json_str) {
    PyErr_Format(PyExc_TypeError, "Expected int");
    return NULL;
  }
  *json_str = endptr;
  if (num_value == (long)num_value) {
    return Py_BuildValue("i", (int)num_value);
  } else {
    return Py_BuildValue("d", num_value);
  }
}

static PyObject *parse_json_value(const char **json_str) {
  *json_str = skip_whitespace(*json_str);
  if (**json_str != '{') {
    PyErr_Format(PyExc_TypeError, "Expected object or value");
    return NULL;
  }
  (*json_str)++;
  *json_str = skip_whitespace(*json_str);

  PyObject *dict = PyDict_New();

  while (**json_str != '}') {
    *json_str = skip_whitespace(*json_str);

    if (**json_str != '"') {
      PyErr_Format(PyExc_TypeError, "Invalid JSON begining \" ");
      return NULL;
    }

    (*json_str)++;
    const char *key_start = *json_str;
    while (**json_str != '"') {
      if (**json_str == '\0') {
        PyErr_Format(PyExc_TypeError, "Unexpected closed \" ");
        return NULL;
      }
      (*json_str)++;
    }
    size_t key_len = *json_str - key_start;
    char *key = malloc(key_len + 1);
    if (!key) {
      return NULL;
    }
    strncpy(key, key_start, key_len);
    key[key_len] = '\0';
    (*json_str)++;

    *json_str = skip_whitespace(*json_str);
    if (**json_str != ':') {
      free(key);
      PyErr_Format(PyExc_TypeError, "Invalid format, expected ':' after key");
      return NULL;
    }
    (*json_str)++;

    *json_str = skip_whitespace(*json_str);
    PyObject *value;
    if (**json_str == '"') {
      value = parse_json_string(json_str);
    } else if (isdigit(**json_str) || **json_str == '-') {
      value = parse_json_numeric(json_str);
    } else {
      PyErr_Format(PyExc_TypeError, "Invalid format, Expected object or value");
      return NULL;
    }
    if (!value) {
      free(key);
      return NULL;
    }

    PyObject *py_key = Py_BuildValue("s", key);
    free(key);
    if (PyDict_SetItem(dict, py_key, value) < 0) {
      return NULL;
    }

    *json_str = skip_whitespace(*json_str);
    if (**json_str == '}') {
      break;
    } else if (**json_str == ',') {
      (*json_str)++;
    } else {
      PyErr_Format(PyExc_TypeError, "Invalid format, expected '}' or ','");
      return NULL;
    }
  }

  return dict;
}

static PyObject *custom_json_loads(PyObject *self, PyObject *args) {
  const char *json_str;
  if (!PyArg_ParseTuple(args, "s", &json_str)) {
    return NULL;
  }

  json_str = skip_whitespace(json_str);
  PyObject *result = parse_json_value(&json_str);

  return result;
}

static PyObject *custom_json_dumps(PyObject *self, PyObject *args) {
  PyObject *dict;

  if (!PyArg_ParseTuple(args, "O!", &PyDict_Type, &dict)) {
    return NULL;
  }

  PyObject *json_list = PyList_New(0);
  if (!json_list) {
    return NULL;
  }

  PyObject *key, *value;
  Py_ssize_t pos = 0;
  while (PyDict_Next(dict, &pos, &key, &value)) {
    PyObject *key_str = PyObject_Str(key);
    if (!key_str) {
      Py_DECREF(json_list);
      return NULL;
    }

    PyObject *key_json = PyUnicode_FromFormat("\"%S\"", key_str);
    if (!key_json) {
      Py_DECREF(key_str);
      Py_DECREF(json_list);
      return NULL;
    }

    PyObject *value_str = PyObject_Str(value);
    if (!value_str) {
      Py_DECREF(key_str);
      Py_DECREF(key_json);
      Py_DECREF(json_list);
      return NULL;
    }

    PyObject *value_json;
    if (PyUnicode_Check(value)) {
      value_json = PyUnicode_FromFormat("\"%S\"", value_str);
    } else {
      value_json = value_str;
      Py_INCREF(value_json);
    }

    PyObject *json_item = PyUnicode_FromFormat("%S: %S", key_json, value_json);
    if (!json_item) {
      Py_DECREF(key_str);
      Py_DECREF(key_json);
      Py_DECREF(value_json);
      Py_DECREF(json_list);
      return NULL;
    }

    PyList_Append(json_list, json_item);

    Py_DECREF(key_str);
    Py_DECREF(key_json);
    Py_DECREF(value_json);
    Py_DECREF(json_item);
  }

  PyObject *json_str = PyUnicode_Join(PyUnicode_FromString(", "), json_list);
  Py_DECREF(json_list);

  if (!json_str) {
    return NULL;
  }

  PyObject *final_str = PyUnicode_FromFormat("{%S}", json_str);
  Py_DECREF(json_str);

  return final_str;
}

static PyMethodDef CustomJsonMethods[] = {
    {"loads", custom_json_loads, METH_VARARGS, "Parser"},
    {"dumps", custom_json_dumps, METH_VARARGS, "Serializer"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef customjsonmodule = {
    PyModuleDef_HEAD_INIT, "custom_json", "Custom JSON", -1, CustomJsonMethods};

PyMODINIT_FUNC PyInit_custom_json(void) {
  return PyModule_Create(&customjsonmodule);
}
