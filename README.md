
# General back project

project with general functions CRUD 


## API Reference

#### Get all items

```http
  GET /user/

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.


## Authors

- [@leoAvella](https://github.com/leoAvella)


## Deployment

To deploy this project run


```bash
  uvicorn main:app --reload
```


## Installation

Install my-project dependencies 

```bash
  pip install -r requirements.txt
  cd my-project
```
    