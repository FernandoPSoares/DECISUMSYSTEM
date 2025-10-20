# backend/app/modules/inventory/products/products_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from .... import models
from . import products_crud, products_schemas

class ProductStructureService:
    # --- Métodos para Categoria de UDM ---
    
    def get_categoria_udm_by_id(self, db: Session, id: str) -> models.CategoriaUdm:
        """Obtém uma Categoria de UDM pelo ID, tratando o caso de não encontrar."""
        db_obj = products_crud.categoria_udm_crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria de UDM não encontrada")
        return db_obj

    def get_all_categorias_udm(self, db: Session, **kwargs) -> List[models.CategoriaUdm]:
        """Obtém todas as Categorias de UDM, passando os filtros para a camada de CRUD."""
        return products_crud.categoria_udm_crud.get_multi(db, **kwargs)

    def create_categoria_udm(self, db: Session, obj_in: products_schemas.CategoriaUdmCreate) -> models.CategoriaUdm:
        """Cria uma Categoria de UDM e a sua unidade de referência obrigatória."""
        if products_crud.categoria_udm_crud.get(db, id=obj_in.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de Categoria de UDM já registado")
        if products_crud.udm_crud.get(db, id=obj_in.unidade_referencia_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID da Unidade de Referência já existe")

        try:
            new_categoria_obj = models.CategoriaUdm(id=obj_in.id, nome=obj_in.nome)
            db.add(new_categoria_obj)
            db.flush()

            udm_ref_obj = models.Udm(
                id=obj_in.unidade_referencia_id,
                nome=obj_in.unidade_referencia_nome,
                proporcao_combinada=1.0,
                categoria_udm_id=new_categoria_obj.id
            )
            db.add(udm_ref_obj)
            db.flush()

            new_categoria_obj.unidade_referencia_id = udm_ref_obj.id
            db.commit()
            db.refresh(new_categoria_obj)
            return new_categoria_obj
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocorreu um erro na transação: {e}")

    def update_categoria_udm(self, db: Session, id: str, obj_in: products_schemas.CategoriaUdmUpdate) -> models.CategoriaUdm:
        """Atualiza os dados de uma Categoria de UDM."""
        db_obj = self.get_categoria_udm_by_id(db, id=id)
        return products_crud.categoria_udm_crud.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def update_categoria_udm_status(self, db: Session, id: str, is_active: bool) -> models.CategoriaUdm:
        """Ativa ou desativa uma Categoria de UDM."""
        db_obj = self.get_categoria_udm_by_id(db, id=id)
        return products_crud.categoria_udm_crud.update_status(db=db, db_obj=db_obj, is_active=is_active)

    # --- Métodos para UDM ---

    def get_udm_by_id(self, db: Session, id: str) -> models.Udm:
        """Obtém uma Unidade de Medida pelo ID, tratando o caso de não encontrar."""
        db_obj = products_crud.udm_crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidade de Medida não encontrada")
        return db_obj

    def get_all_udm(self, db: Session, **kwargs) -> List[models.Udm]:
        """Obtém todas as Unidades de Medida, passando os filtros para a camada de CRUD."""
        return products_crud.udm_crud.get_multi(db, **kwargs)

    def create_udm(self, db: Session, obj_in: products_schemas.UdmCreate) -> models.Udm:
        """Cria uma nova Unidade de Medida (que não seja de referência)."""
        if products_crud.udm_crud.get(db, id=obj_in.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de Unidade de Medida já registado")
        
        # Validação de negócio: verifica se a categoria existe
        self.get_categoria_udm_by_id(db, id=obj_in.categoria_udm_id)
        
        return products_crud.udm_crud.create(db=db, obj_in=obj_in)

    def update_udm(self, db: Session, id: str, obj_in: products_schemas.UdmUpdate) -> models.Udm:
        """Atualiza os dados de uma Unidade de Medida."""
        db_obj = self.get_udm_by_id(db, id=id)
        return products_crud.udm_crud.update(db=db, db_obj=db_obj, obj_in=obj_in)
        
    def update_udm_status(self, db: Session, id: str, is_active: bool) -> models.Udm:
        """Ativa ou desativa uma Unidade de Medida."""
        db_obj = self.get_udm_by_id(db, id=id)
        # Regra de negócio: Impede a desativação da unidade de referência
        if not is_active and db_obj.id == db_obj.categoria_udm.unidade_referencia_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível desativar a unidade de referência de uma categoria.")
        return products_crud.udm_crud.update_status(db=db, db_obj=db_obj, is_active=is_active)

    # --- Métodos para Categoria de Produto ---

    def get_categoria_produto_by_id(self, db: Session, id: str) -> models.CategoriaProduto:
        """Obtém uma Categoria de Produto pelo ID."""
        db_obj = products_crud.categoria_produto_crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria de Produto não encontrada")
        return db_obj

    def get_all_categorias_produto(self, db: Session, **kwargs) -> List[models.CategoriaProduto]:
        """Obtém todas as Categorias de Produto."""
        return products_crud.categoria_produto_crud.get_multi(db, **kwargs)

    def create_categoria_produto(self, db: Session, obj_in: products_schemas.CategoriaProdutoCreate) -> models.CategoriaProduto:
        """Cria uma nova Categoria de Produto."""
        if products_crud.categoria_produto_crud.get(db, id=obj_in.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de Categoria de Produto já registado")
        
        if obj_in.categoria_pai_id:
            self.get_categoria_produto_by_id(db, id=obj_in.categoria_pai_id)
            
        return products_crud.categoria_produto_crud.create(db=db, obj_in=obj_in)

    def update_categoria_produto(self, db: Session, id: str, obj_in: products_schemas.CategoriaProdutoUpdate) -> models.CategoriaProduto:
        """Atualiza os dados de uma Categoria de Produto."""
        db_obj = self.get_categoria_produto_by_id(db, id=id)
        return products_crud.categoria_produto_crud.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def update_categoria_produto_status(self, db: Session, id: str, is_active: bool) -> models.CategoriaProduto:
        """Ativa ou desativa uma Categoria de Produto."""
        db_obj = self.get_categoria_produto_by_id(db, id=id)
        return products_crud.categoria_produto_crud.update_status(db=db, db_obj=db_obj, is_active=is_active)

# Cria uma instância do serviço para ser usada pelos routers
product_structure_service = ProductStructureService()

